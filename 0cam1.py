# -*- coding: utf-8 -*-
"""
Created on Mon May 15 04:57:22 2023

@author: rando
"""
import sys, random

split_ops = "$+-*/%=?:{([,>&|!<~._\\"
ops = "+-*/%=?:,>&|!~_.\\"
digs = "0123456789"


def tokenise(source, file=True):
    
    if file:
        source = source.replace("\n", " ") + ","
    for i in split_ops:
        source = source.replace(i, " " + i + " ")
    source = source + " "
    prev_source = source
    source = source.replace("  ", " ")
    while source != prev_source:
        prev_source = source
        source = source.replace("  ", " ")
    
    # prev_char = ""
    token = ""
    tokens = []
    
    brackets = 0
    bracket = ""
    
    def add_token():
        nonlocal token, tokens
        if token[0] in digs:
            try:
                int_token = int(token)
                if len(tokens) == 1 and tokens[-1] == ("-", "-"):
                    tokens[-1] = ("int", -int_token)
                elif len(tokens) > 1 and tokens[-1] == ("-", "-") and tokens[-2][0] not in ("int", "brac", "empty"):
                    tokens[-1] = ("int", -int_token)
                else:
                    tokens.append(("int", int_token))
            except:
                pass
        elif token in ops + "$<":
            if len(tokens) > 0 and tokens[-1] == ("?", "?") and token == "?":
                tokens[-1] = ("rand", "??")
            else:
                tokens.append((token, token))
        token = ""
        
    for i in source:
        if brackets == 0:
            if i == " ":
                if token != "":
                    add_token()
            elif i == "{":
                brackets += 1
                bracket = "{"
            elif i == "(":
                brackets += 1
                bracket = "("
            elif i == "[":
                brackets += 1
                bracket = "["
            elif i in digs+ops+"$<":
                token += i
            elif i in ")}]":
                raise Exception("Mismatched bracket " + i)
        else:
            if bracket == "{":
                if i in digs+split_ops+")]":
                    raise Exception("Something in trivial")
                elif i == "}":
                    tokens.append(("triv", "{}"))
                    brackets -= 1
                    bracket = ""
            elif bracket == "(":
                token += i
                if i == "(":
                    brackets += 1
                if i == ")":
                    brackets -= 1
                    if brackets == 0:
                        bracket = ""
                        bracket_tokens = tokenise(token[:-1], False)
                        if len(bracket_tokens) == 0:
                            tokens.append(("unit", "()"))
                        else:
                            tokens.append(("brac", bracket_tokens))
            elif bracket == "[":
                if i in digs+split_ops+"})":
                    raise Exception("Something in empty")
                elif i == "]":
                    tokens.append(("empty", "[]"))
                    brackets -= 1
                    bracket = ""
    if brackets != 0:
        raise Exception("End of file when scanning brackets")
    
    return tokens


op_heirarchy = {"&": -2, "|": -2, "+": 0, "-": 0, "*": 2, "/": 2, "\\": 2, "%": 2, ">": -200, "?": -100, ":": 10000, "func_call": 1000}


def split_list(l, splitter):
    result = []
    temp = []
    for i in l:
        if i == splitter and len(temp) > 0:
            result.append(temp)
            temp = []
        else:
            temp.append(i)
    if len(temp) != 0:
        result.append(temp)
    return result


def conv_tokens_to_string(tokens):
    if isinstance(tokens, list):
        return " ".join([conv_tokens_to_string(i) for i in tokens])
    elif tokens[0] == "int":
        return str(tokens[1])
    elif tokens[0] == "brac":
        return "(" + conv_tokens_to_string(tokens[1]) + ")"
    elif tokens[0] in ["$", "+", "-", "*", "/", "%", "=", "?", ":", "{", "(", 
                       "[", ",", ">", "&", "|", "!", "<", "~", ".", "_", "\\", 
                       "unit", "empty", "triv"]:
        return str(tokens[1])
    raise Exception("MISSING CASE IN CONV TOKENS TO STRING " + str(tokens[0]))


def syntax_tree(tokens, state):
    if state == "file":
        lines = []
        line = []
        for i in tokens:
            if i[0] == ",":
                if len(line) != 0:
                    try:
                        lines.append(syntax_tree(line, "line"))
                        line = []
                    except Exception as e:
                        try:
                            print("Exception " + str(e) + " when parsing line " + conv_tokens_to_string(line))
                        except Exception as e:
                            print("Exeption " + str(e) + " when converting line")
                        return []
            else:
                line.append(i)
        return lines
    
    elif state == "line":
        if ("=", "=") in tokens:
            ind = tokens.index(("=", "="))
            if ind == 1:
                if tokens[0] == ("_", "_"):
                    splits = split_list(tokens[ind+1:], ("!", "!"))
                    patterns = []
                    for i in splits:
                        patterns.append(syntax_tree(i, "handle_t"))
                    return ("type", patterns)
                elif tokens[0] == ("triv", "{}"):
                    return ("assign", syntax_tree(tokens[:ind], "handle"), syntax_tree(tokens[ind+1:], "params"))
                elif tokens[0] == ("$", "$"):
                    return ("assign", syntax_tree(tokens[:ind], "handle"), syntax_tree(tokens[ind+1:], "params"))
            return ("assign", syntax_tree(tokens[:ind], "handle"), syntax_tree(tokens[ind+1:], "expr"))
        else:
            return syntax_tree(tokens, "expr")
        
    elif state == "handle":
        if len(tokens) == 1:
            return ("name", syntax_tree([tokens[0]], "expr"))
        elif len(tokens) == 2:
            if tokens[0][0] == "-":
                return ("name", syntax_tree(tokens, "expr"))
        evaluated = []
        for i in tokens:
            evaluated.append(syntax_tree([i], "expr"))
        return ("handle", evaluated[0], evaluated[1:])
    
    elif state == "handle_t":
        evaluated = []
        for i in tokens:
            evaluated.append(syntax_tree([i], "expr"))
        return ("handle_t", evaluated[0], evaluated[1:])
    
    elif state == "match_case":
        evaluated = []
        for i in tokens:
            evaluated.append(syntax_tree([i], "expr"))
        return ("match_t", evaluated[0], evaluated[1:])
    
    elif state == "params":
        evaluated = []
        for i in tokens:
            evaluated.append(syntax_tree([i], "expr"))
        return ("params", evaluated)
    
    elif state == "match":
        ind = tokens.index((">", ">"))
        return ("match", syntax_tree(tokens[:ind], "match_case"), syntax_tree(tokens[ind+1:], "expr"))
    
    elif state == "scope_a":
        if ("~", "~") in tokens:
            ind = tokens.index(("~", "~"))
            if ind == 1:
                if tokens[0] == ("_", "_"):
                    splits = split_list(tokens, ("!", "!"))
                    patterns = []
                    for i in splits:
                        patterns.append(syntax_tree(i, "handle"))
                    return ("type", patterns)
                elif tokens[0] == ("triv", "{}"):
                    return ("assign", syntax_tree(tokens[:ind], "handle"), syntax_tree(tokens[ind+1:], "params"))
                elif tokens[0] == ("$", "$"):
                    return ("assign", syntax_tree(tokens[:ind], "handle"), syntax_tree(tokens[ind+1:], "params"))
            return ("assign", syntax_tree(tokens[:ind], "handle"), syntax_tree(tokens[ind+1:], "expr"))
        else:
            return syntax_tree(tokens, "expr")
    
    elif state == "expr":
        if ("!", "!") in tokens:
            splits = split_list(tokens, ("!", "!"))
            patterns = []
            for i in splits[1:]:
                patterns.append(syntax_tree(i, "match"))
            return ("pattern", syntax_tree(splits[0], "expr"), patterns)
        elif (".", ".") in tokens and ("?", "?") not in tokens:
            splits = split_list(tokens, (".", "."))
            assigns = []
            for i in splits[:-1]:
                assigns.append(syntax_tree(i, "scope_a"))
            return ("scope_a", assigns, syntax_tree(splits[-1], "expr"))
        elif len(tokens) == 1:
            if tokens[0][0] == "int":
                return tokens[0]
            elif tokens[0][0] == "brac":
                res = syntax_tree(tokens[0][1], "expr")
                if res[0] == "int":
                    return ("intf", ("int", res[1]))
                return res
            elif tokens[0][0] in ["unit", "triv", "$", "<", "empty", "rand"]:
                return tokens[0]
            elif tokens[0][0] == "+":
                return ("::", "+")
            elif tokens[0][0] in ["=", "~"]:
                raise Exception("Invalid assignment in expression")
        else:
            op = "func_call"
            prev_i = ""
            for i in tokens:
                if i[0] in ops and prev_i not in ops:
                    if i[0] in op_heirarchy.keys():
                        if op_heirarchy[i[0]] < op_heirarchy[op]:
                            op = i[0]
                prev_i = i[0]
            if op == "func_call":
                if len(tokens) > 1:
                    if tokens[0][0] == "-":
                        return ("neg", syntax_tree(tokens[1:], "expr"))
                    elif tokens[0][0] == "*":
                        return ("star", syntax_tree(tokens[1:], "expr"))
                evaluated = []
                for i in tokens:
                    evaluated.append(syntax_tree([i], "expr"))
                return ("func_call", evaluated[0], evaluated[1:])
            elif op == "?":
                ind1 = tokens.index(("?", "?"))
                ind2 = tokens.index((":", ":"))
                return ("cond", 
                        syntax_tree(tokens[:ind1], "expr"), 
                        syntax_tree(tokens[ind1 + 1: ind2], "expr"), 
                        syntax_tree(tokens[ind2 + 1:], "expr"))
            elif op == ">":
                ind = tokens.index((">", ">"))
                return ("a_func", syntax_tree(tokens[:ind], "params"), syntax_tree(tokens[ind+1:], "expr"))
            elif op in "+-/*%&|\\":
                ind = tokens.index((op, op))
                return (op, 
                        syntax_tree(tokens[: ind], "expr"), 
                        syntax_tree(tokens[ind + 1:], "expr"))
        raise Exception("MISSING CASE IN PARSING " + conv_tokens_to_string(tokens) + " IN STATE " + state)
            
class Output:
    
    def __init__(self, print_enabled = True):
        self.output_text = ""
        self.print_enabled = print_enabled
        
    def write(self, string):
        self.output_text += string + "\n"
        if self.print_enabled:
            print(string)


# Executes the partially compiled code
# Returns the outputs and the final context
def execute(tree_code):
    output = Output(True)
    error_output = Output(True)
    context = {}
    for i in tree_code:
        try:
            assign_to_scope(i, context, output)
        except Exception as e:
            try:
                error_output.write("Exception " + str(e) + " when executing line: " + conv_to_code(i) + ".")
            except Exception as e:
                error_output.write("Exception " + str(e) + " when converting code.")
            
    return output.output_text, error_output.output_text, context


def conv_to_code(value, direct = True):
    if isinstance(value, list):
        return ",\n".join([conv_to_code(i) for i in value])
    elif value[0] == "int":
        return str(value[1])
    elif value[0] == "intf":
        return conv_to_code(value[1])
    elif value[0] == "unit":
        return "()"
    elif value[0] == "brac":
        return "(" + conv_to_code(value[1]) + ")"
    elif value[0] == "triv":
        return "{}"
    elif value[0] == "empty":
        return "[]"
    elif value[0] == "name":
        return conv_to_code(value[1])
    elif value[0] == "rand":
        return "??"
    elif value[0] in "+-/*%&|\\":
        return conv_to_code(value[1]) + value[0] + conv_to_code(value[2])
    elif value[0] == "neg":
        return "- " + conv_to_code(value[1])
    elif value[0] == "star":
        return "* " + conv_to_code(value[1])
    elif value[0] in "<$":
        return value[0]
    elif value[0] == "::":
        return "+"
    elif value[0] == "scope_a":
        return ".".join([conv_to_code(i, False) for i in value[1]]) + "." + conv_to_code(value[2])
    elif value[0] in ["handle", "handle_t", "match_t", "func_call", "handle_t"]:
        return conv_to_code(value[1]) + " " + " ".join([conv_to_code(i) for i in value[2]])
    elif value[0] == "params":
        return " ".join([conv_to_code(i) for i in value[1]])
    elif value[0] == "assign":
        if direct:
            return conv_to_code(value[1]) + "=" + conv_to_code(value[2])
        return conv_to_code(value[1]) + "~" + conv_to_code(value[2])
    elif value[0] == "pattern":
        return conv_to_code(value[1]) + "!" + "!".join([conv_to_code(i) for i in value[2]])
    elif value[0] in ["match", "a_func"]:
        return conv_to_code(value[1]) + ">" + conv_to_code(value[2])
    elif value[0] == "type":
        return "!".join([conv_to_code(i) for i in value[1]])
    elif value[0] == "cond":
        return conv_to_code(value[1]) + "?" + conv_to_code(value[2]) + ":" + conv_to_code(value[3])
    elif value[0] == "part_f":
        return "(" + conv_to_code(value[1]) + ") " + " ".join([conv_to_code(i) for i in value[2]])
    raise Exception("MISSING CASE IN CONV_CODE " + str(value))


def conv_list_to_string(value, start = True):
    output = ""
    if start:
        output = "["
    if value[0] == "type":
        if value[1] == []:
            return "]"
    elif value[0] == "cons":
        if value[1] == []:
            return output + "]"
        elif value[1] == "+":
            if not start:
                output += ", "
            output += conv_to_string(value[2][0])
            return output + conv_list_to_string(value[2][1], False)
    raise Exception("Invalid list conversion")


def conv_to_chars(value, context, output):
    if value[0] == "int":
        return chr(value[1])
    elif value[0] == "type":
        if value[1] == []:
            return ""
    elif value[0] == "cons":
        if value[1] == []:
            return ""
        elif value[1] == "+":
            res = eval_expr(value[2][0], context, output)
            if res[0] == "int":
                return chr(res[1]) + conv_to_chars(value[2][1], context, output)
            elif res[0] == "cons":
                return conv_to_chars(res, context, output) + conv_to_chars(value[2][1], context, output)
    raise Exception("Attempted to convert character non-convertible " + conv_to_string(value))


def conv_to_string(value):
    if value[0] == "int":
        return str(value[1])
    elif value[0] == ():
        return "()"
    elif value[0] == "func":
        output = ""
        for i in value[1]:
            output += conv_to_string(i) + " "
        return output + "> " + conv_to_code(value[2])
    elif value[0] == "cons":
        if value[1] in ["+", []]:
            return conv_list_to_string(value)
        output = ""
        for i in value[2]:
            output += conv_to_code(i) + " "
        output = output[:-1]
        return str(value[1]) + " " + output
    elif value[0] == "type":
        output = ""
        for i in value[1]:
            output += conv_to_string(i) + " "
        return output + "!"
    else:
        raise Exception("Unprintable type" + str(value))
    raise Exception("MISSING PRINT CASE")


def assign_to_scope(tree, context, output):
    
    if tree[0] == "assign":
        name = tree[1]
        
        if name[0] == "name":
            res = None
            if name[1][0] == "int":
                res = name[1]
            elif name[1][0] == "triv":
                for j in tree[2][1]:
                    if j[0] != "int":
                        raise Exception("Attempted to trivialise non-int")
                    if j[1] in context.keys():
                        context.pop(j[1])
                return
            elif name[1][0] == "$":
                output_string = ""
                for j in tree[2][1]:
                    output_string += conv_to_chars(eval_expr(j, context, output), context, output)
                output.write(output_string)
                return
            else:
                res = eval_expr(name[1], context, output)
            if res[0] != "int":
                raise Exception("Attempted to assign to non-int")
            if tree[2][0] == "int":
                context[res[1]] = tree[2]
            else:
                context[res[1]] = ("intf", tree[2])
                
        elif name[0] == "handle":
            if name[1][0] == "int":
                res = name[1]
            else:
                res = eval_expr(name[1], context, output)
            if res[0] != "int":
                raise Exception("Attempted to assign to non-int")
            evaluated = []
            for j in name[2]:
                if j[0] == "int":
                    evaluated.append(j)
                else:
                    evaluated.append(eval_expr(j, context, output))
            context[res[1]] = ("func", evaluated, tree[2])
        else:
            raise Exception("Invalid assignment value")
            
    elif tree[0] == "type":
        for j in tree[1]:
            name = j
            if name[0] == "handle_t":
                if name[1][0] == "int":
                    res = name[1]
                else:
                    res = eval_expr(name[1], context, output)
                if res[0] != "int":
                    raise Exception("Attempted to assign to non-int")
                evaluated = []
                for j in name[2]:
                    if j[0] == "int":
                        evaluated.append(j)
                    else:
                        evaluated.append(eval_expr(j, context, output))
                context[res[1]] = ("type", evaluated, ())
    else:
        res = eval_expr(tree, context, output)
        output.write(conv_to_string(res))


# Matches a case
def match_case(value, case, context, output):
    if case[0] == "match_t":
        res = eval_expr(case[1], context, output, True)
        if res[0] != "name":
            raise Exception("INVALID NAME RETURN")
        else:
            _, name, val = res
            if val[0] == "type":
                if value[0] == "cons":
                    if name != value[1]:
                        return False, context
                    for i in range(len(case[2])):
                        res1 = eval_expr(case[2][i], context, output)
                        res2 = eval_expr(value[2][i], context, output)
                        if res1 != res2:
                            return False, context
                    
                    if (len(case[2]) == len(val[1])):
                        return True, context
                    temp_context = context.copy()
                    for i in range(len(case[2]), len(val[1])):
                        res = val[1][i]
                        if res[0] != ():
                            if res[0] != "int":
                                raise Exception("Attempted to assign to non-int")
                            temp_context[res[1]] = eval_expr(value[2][i], context, output)
                    return True, temp_context
                else:
                    raise Exception("Attempted to compare a constructor to a non-constructor")
                    
            elif val[0] == "int":
                if value[0] != "int":
                    raise Exception("Attempted to compare an int to a non-int")
                if val[1] == value[1]:
                    return True, context
                
            elif val[0] == "func":
                if value[0] == "func":
                    pass
                elif value[0] == "type":
                    pass
                
            elif val[0] == "cons":
                if val[2] == []:
                    if value[0] in ("cons", "int"):
                        return (name == value[1]), context
                    
            raise Exception("Missing match case " + str(val[0]) + " with " + str(value[0]))
    else:
        raise Exception("Attempted to match a non-case")


def flatten_partial_cons(res):
    if res[0] == "type":
        if res[2] == ():
            return (), []
        else:
            name, params = flatten_partial_cons(res[2])
            return name, params
        
    elif res[0] == "part_c":
        name, params = flatten_partial_cons(res[2])
        if res[1] != ():
            name = res[1]
        return name, params + res[3]
    raise Exception("Invalid partial constructor evaluation")


# Can return two things: either a function, or an integer
# Used to actually finally execute code, instead of just creating assignments
# ("int", final int value), 
# ("func", param_names, expr)
# ("type", params, base) a type constructor
# ("cons", name, params) a constructed object
def eval_expr(tree, context, output, get_name = False):
    
    #Evaluate a function call
    if tree[0] == "func_call":
        name = tree[1]
        params = tree[2]
        res = eval_expr(name, context, output, True)
        if res[0] != "name":
            raise Exception("INVALID NAME RETURN")
        func_name = res[1]
        res = res[2]
        if res[0] == "func":
            param_names = res[1]
            expr = res[2]
            if expr == ("???"):
                if len(params) == 0:
                    if get_name:
                        return ("name", (), ("int", random.randint(0, 1)))
                    return ("int", random.randint(0, 1))
                elif len(params) == 1:
                    res = eval_expr(params[0], context, output)
                    if res[0] != "int":
                        raise Exception("Attempted to bound random with non-int")
                    if get_name:
                        return ("name", (), ("int", random.randint(0, res[1])))
                    return ("int", random.randint(0, res[1]))
                elif len(params) == 2:
                    res1 = eval_expr(params[0], context, output)
                    res2 = eval_expr(params[1], context, output)
                    if res1[0] != "int":
                        raise Exception("Attempted to bind random with non-int")
                    if res2[0] != "int":
                        raise Exception("Attempted to bind random with non-int")
                    if get_name:
                        return ("name", (), ("int", random.randint(res1[1], res2[1])))
                    return ("int", random.randint(res1[1], res2[1]))
                else:
                    raise Exception("Too many arguments for function")
            elif len(params) == len(param_names):
                temp_context = context.copy()
                for i in range(len(params)):
                    res = param_names[i]
                    if res[0] != ():
                        if res[0] != "int":
                            raise Exception("Attempted to assign to non-int")
                        temp_context[res[1]] = eval_expr(params[i], context, output)
                return eval_expr(expr, temp_context, output, get_name)
            elif len(params) < len(param_names):
                if get_name:
                    return ("name", (), ("func", param_names[len(params):], ("part_f", param_names[:len(params)], params, expr)))
                return ("func", param_names[len(params):], ("part_f", param_names[:len(params)], params, expr))
            else:
                raise Exception("Too many arguments for function")
        elif res[0] == "type":
            param_names = res[1]
            if len(params) == len(param_names):
                if res[2] == ():
                    return ("cons", func_name, params)
                else:
                    name, part_params = flatten_partial_cons(res)
                    return ("cons", name, part_params + params)
            elif len(params) < len(param_names):
                if get_name:
                    return ("name", (), ("type", param_names[len(params):], ("part_c", func_name, res, params)))
                return ("type", param_names[len(params):], ("part_c", func_name, res, params))
            else:
                raise Exception("Too many arguments for constructor")
        elif res[0] == "cons":
            if res[2] == []:
                if len(params) == 0:
                    return res
                else:
                    raise Exception("Too many arguments for constructor")
            else:
                raise Exception("Attempted to execute non-executable")
        raise Exception("Attempted to execute non-executable")
    
    elif tree[0] == "part_f":
        param_names = tree[1]
        params = tree[2]
        expr = tree[3]
        temp_context = context.copy()
        for i in range(len(params)):
            res = param_names[i]
            if res[0] != ():
                if res[0] != "int":
                    raise Exception("Attempted to assign to non-int")
                temp_context[res[1]] = eval_expr(params[i], context, output)
        return eval_expr(expr, temp_context, output, get_name)
    
    elif tree[0] == "scope_a":
        temp_context = context.copy()
        for i in tree[1]:
            assign_to_scope(i, temp_context, output)
        return eval_expr(tree[2], temp_context, output, get_name)
    
    elif tree[0] == "pattern":
        val = eval_expr(tree[1], context, output)
        cases = tree[2]
        for i in cases:
            if i[0] != "match":
                # May change behaviour
                raise Exception ("Attempted to match a non-match case")
            matched, new_context = match_case(val, i[1], context, output)
            if matched:
                return eval_expr(i[2], new_context, output, get_name)
        raise Exception ("Failed to match a case")
    
    elif tree[0] == "a_func":
        if tree[1][0] != "params":
            raise Exception("Attempted to invalid anonymous function")
        param_names = tree[1][1];
        eval_names = []
        for i in param_names:
            res = eval_expr(i, context, output)
            if res[0] == "func":
                raise Exception("Attempted to assign to funtion")
            eval_names.append(res)
        if get_name:
            return ("name", (), ("func", eval_names, tree[2]))
        return ("func", eval_names, tree[2])
    
    elif tree[0] == "cond":
        cond = tree[1]
        res = eval_expr(cond, context, output)
        if res[0] != "int":
            print(tree, "\n", res)
            raise Exception("Attempted to compare to a non-int")
        if res[1] <= 0:
            return eval_expr(tree[2], context, output, get_name)
        else:
            return eval_expr(tree[3], context, output, get_name)
        
    elif tree[0] in "+-/*%&|\\":
        res1 = eval_expr(tree[1], context, output)
        res2 = eval_expr(tree[2], context, output)
        if res1[0] == res2[0] == "int":
            res = None
            if tree[0] == "+":
                res = res1[1] + res2[1]
            elif tree[0] == "-":
                res = res1[1] - res2[1]
            elif tree[0] == "/":
                res = res1[1] // res2[1]
            elif tree[0] == "*":
                res = res1[1] * res2[1]
            elif tree[0] == "%":
                res = res1[1] % res2[1]
            elif tree[0] == "&":
                res = res1[1] & res2[1]
            elif tree[0] == "|":
                res = res1[1] | res2[1]
            elif tree[0] == "\\":
                res = res2[1] // res1[1]
            return eval_expr(("int", res), context, output, get_name)
        elif res1[0] == "func" and res2[0] == "func":
            if get_name:
                return ("name", (), ("func", res1[1] + res2[1], (tree[0], res1[2], res2[2])))
            return ("func", res1[1] + res2[1], (tree[0], res1[2], res2[2]))
        elif res1[0] == "int" and res2[0] == "func":
            if get_name:
                return ("name", (), ("func", res2[1], (tree[0], res1, res2[2])))
            return ("func", res2[1], (tree[0], res1, res2[2]))
        elif res1[0] == "func" and res2[0] == "int":
            if get_name:
                return ("name", (), ("func", res1[1], (tree[0], res1[2], res2)))
            return ("func", res1[1], (tree[0], res1[2], res2))
        elif res2[0] == "cons":
            if tree[0] == "+" and (res2[1] in [[], "+"]):
                if get_name:
                    return ("name", (), ("cons", "+", [res1, res2]))
                return ("cons", "+", [res1, res2])
                
            raise Exception("Invalid operator combination")
        elif res1[0] == () or res2[0] == ():
            return ((), ())
        else:
            raise Exception("Invalid operator combination " + str(res1[0]) + " " + str(res2[0]))
    
    elif tree[0] == "neg":
        res = eval_expr(tree[1], context, output)
        if res[0] == "int":
            return eval_expr(("int", -res[1]), context, output, get_name)
        if res[0] == "cons" and res[1] == "+":
            if get_name:
                return ("name", (), res[2][1])
            return res[2][1]
        raise Exception("Attempted to negate an invalid object")
    
    elif tree[0] == "star":
        res = eval_expr(tree[1], context, output)
        if res[0] == "cons" and res[1] == "+":
            if get_name:
                return ("name", (), res[2][0])
            return res[2][0]
        raise Exception("Attempted to star an invalid object")
    
    elif tree[0] == "type":
        if get_name:
            return ("name", (), tree)
        return tree
    
    elif tree[0] == "int":
        if tree[1] in context.keys():
            val = context[tree[1]]
            if val[0] == "int" or val[0] == "intf":
                return eval_expr(val, context, output, get_name)
            elif get_name == False:
                if val[0] == "type" and val[1] == []:
                    return ("cons", tree[1], [])
                return val
            else:
                return ("name", tree[1], val)
        else:
            if get_name:
                return("name", (), ("int", tree[1]))
            return ("int", tree[1])
        
    elif tree[0] == "intf":
        return eval_expr(tree[1], context, output, get_name)
    
    elif tree[0] == "empty":
        if get_name:
            return ("name", [], ("type", [], ()))
        return ("cons", [], [])
    
    elif tree[0] == "::":
        if get_name:
            return ("name", "+", ("type", [((), ()), ((), ())]))
        return ("type", [((), ()), ((), ())], ())
    
    elif tree[0] == "<":
        if get_name:
            return ("name", (), ("int", int(input())))
        return ("int", int(input()))
    
    elif tree[0] == "rand":
        if get_name:
            return ("name", (), ("func", [], ("???")))
        return ("int", random.randint(0, 1))
    
    elif tree[0] == "unit":
        if get_name:
            return("name", (), ((), ()))
        return ((), ())
    
    else:
        raise Exception("Invalid expression type " + str(tree[0]))
    raise Exception("MISSING EVALUATION CASE")

filename = "input.m1"
if (len(sys.argv) >= 2):
    filename = sys.argv[1]
text = ""
with open(filename, "rb") as code:
    text = code.read().decode("utf-8")
    
if text == "":
    print("Empty code")
else:
    tokenised_code = []
    try:
        tokenised_code = tokenise(text)
    except Exception as e:
        print("Exception " + str(e) + " when tokenising")
    # print("Tokens: ", tokenised_code)
    if tokenised_code == []:
        print("Empty code")
    else:
        tree_code = syntax_tree(tokenised_code, "file")
        
        if tree_code == []:
            print("Failed to parse file")
        else:
            filename = "code.m1"
            if (len(sys.argv) >= 3):
                filename = sys.argv[2]
            with open(filename, "w") as code_file:
                code_file.write(conv_to_code(tree_code))
                
            # print("Tree: ", tree_code)
            # print("--==EXECUTING==--")
            output, errors, final_context = execute(tree_code)
            # print("--==FINISHED==--")
            # print(final_context)
            
            filename = "output.txt"
            if (len(sys.argv) >= 4):
                filename = sys.argv[3]
            with open(filename, "w") as output_file:
                output_file.write(output)
                
            filename = "error.txt"
            if (len(sys.argv) >= 5):
                filename = sys.argv[4]
            with open(filename, "w") as error_file:
                error_file.write(errors)
