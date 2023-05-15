# -*- coding: utf-8 -*-
"""
Created on Mon May 15 04:57:22 2023

@author: rando
"""
import copy, sys

split_ops = "$+-*/%=?:{(,>&|"
ops = "$+-*/%=?:,>&|"
digs = "0123456789"


def tokenise(source, file=True):
    
    if file:
        source = source.replace("\n", " ") + ","
    for i in split_ops:
        source = source.replace(i, " "+i+" ")
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
        # print("Adding tokens: ", token)
        if token[0] in digs:
            try:
                tokens.append(("int", int(token)))
            except:
                pass
        if token in ops:
            tokens.append((token, token))
        token = ""
    # print(source)
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
            elif i in digs+ops:
                token += i
            elif i in ")}":
                raise Exception("Mismatched bracket " + i)
        else:
            if bracket == "{":
                if i in digs+ops+"{()":
                    raise Exception("Something in {}")
                elif i == "}":
                    tokens.append(("triv", "{}"))
                    brackets -= 1
                    bracket = ""
            elif bracket == "(":
                token += i
                if i == "(":
                    brackets += 1
                    pass
                if i == ")":
                    brackets -= 1
                    if brackets == 0:
                        bracket = ""
                        tokens.append(("brac", tokenise(token[:-1], False)))
    if brackets != 0:
        raise Exception("End of file when scanning brackets")
        
    return tokens

op_heirarchy = {"&": -2, "|": -2, "+": 0, "-": 0, "*": 2, "/": 2, "%": 2, ">": -200, "?": -100, ":": 100000, "func_call": 1000}

def syntax_tree(tokens, state):
    
    if state == "file":
        lines = []
        line = []
        for i in tokens:
            if i[0] == ",":
                if len(line) != 0:
                    lines.append(syntax_tree(line, "line"))
                    line = []
            else:
                line.append(i)
        return lines
    
    elif state == "line":
        if ("=", "=") in tokens:
            ind = tokens.index(("=", "="))
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
    
    elif state == "params":
        evaluated = []
        for i in tokens:
            evaluated.append(syntax_tree([i], "expr"))
        return ("params", evaluated)
    
    elif state == "expr":
        if len(tokens) == 1:
            if tokens[0][0] == "int":
                return tokens[0]
            elif tokens[0][0] == "brac":
                return syntax_tree(tokens[0][1], "expr")
            elif tokens[0][0] == "triv":
                return tokens[0]
            elif tokens[0][0] == "$":
                return tokens[0]
        else:
            op = "func_call"
            prev_i = ""
            for i in tokens:
                if i[0] in ops and prev_i not in ops:
                    if op_heirarchy[i[0]] < op_heirarchy[op]:
                        op = i[0]
                prev_i = i[0]
            if op == "func_call":
                if len(tokens) == 2:
                    if tokens[0][0] == "-":
                        return ("neg", syntax_tree([tokens[1]], "expr"))
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
            elif op ==">":
                ind = tokens.index((">", ">"))
                return ("a_func", syntax_tree(tokens[:ind], "params"), syntax_tree(tokens[ind+1:], "expr"))
            elif op in "+-/*%&|":
                ind = tokens.index((op, op))
                return (op, 
                        syntax_tree(tokens[: ind], "expr"), 
                        syntax_tree(tokens[ind + 1:], "expr"))


# Executes the partially compiled code
# Returns the outputs and the final context
def execute(tree_code):
    output_text = ""
    base_context = {}
    for i in tree_code:
        
        if i[0] == "assign":
            name = i[1]
            if name[0] == "name":
                res = None
                if name[1][0] == "int":
                    res = name[1]
                else:
                    res = evaluate_expr(name[1], base_context)
                if res[0] == "func":
                    raise Exception("Attempted to assign to funtion")
                if i[2][0] == "int":
                    base_context[res[1]] = i[2]
                else:
                    base_context[res[1]] = ("intf", i[2])
            elif name[0] == "handle":
                if name[1][0] == "int":
                    res = name[1]
                else:
                    res = evaluate_expr(name[1], base_context)
                if res[0] == "func":
                    raise Exception("Attempted to assign to funtion")
                evaluated = []
                for j in name[2]:
                    if j[0] == "int":
                        evaluated.append(j)
                    else:
                        evaluated.append(evaluate_expr(j, base_context))
                base_context[res[1]] = ("func", evaluated, i[2])
                
        else:
            triv = False
            if i[0] == "func_call":
                if i[1] == ("triv", "{}"):
                    triv = True
                    for j in i[2]:
                        if j[0] != "int":
                            raise Exception("Attempted to trivialise non-int")
                        if j[1] in base_context.keys():
                            base_context.pop(j[1])
                            
                elif i[1] == ("$", "$"):
                    triv = True
                    output_string = ""
                    for j in i[2]:
                        res = evaluate_expr(j, base_context)
                        if res[0] == "int":
                            output_string += chr(res[1])
                        else:
                            raise Exception("Attempted to print a function")
                    print(output_string)
                    output_text += output_string + "\n"
                    
            if not triv:
                res = evaluate_expr(i, base_context)
                if res[0] == "int":
                    print(res[1])
                    output_text += str(res[1]) + "\n"
                else:
                    print(len(res[1]), ">")
                    output_text += str(len(res[1])) + " >\n"
            
    return output_text, base_context


# Can return two things: either a function, or an integer
# Used to actually finally execute code, instead of just creating assignments
# ("int", final int value), ("func", a functional value that still needs to be finally evaluated)
def evaluate_expr(tree, context):
    
    if tree[0] == "func_call":
        name = tree[1]
        params = tree[2]
        res = evaluate_expr(name, context)
        if res[0] == "int":
            raise Exception("Attempted to execute an integer");
        param_names = res[1]
        expr = res[2]
        if len(params) == len(param_names):
            temp_context = copy.copy(context)
            for i in range(len(params)):
                res = param_names[i]
                if res[0] == "func":
                    raise Exception("Attempted to assign to funtion")
                temp_context[res[1]] = evaluate_expr(params[i], context)
            return evaluate_expr(expr, temp_context)
        elif len(params) < len(param_names):
            return ("func", param_names[len(params):], ("part", param_names[:len(params)], params, expr))
        else:
            raise Exception("Too many argument for function")
    
    elif tree[0] == "part":
        param_names = tree[1]
        params = tree[2]
        expr = tree[3]
        temp_context = copy.copy(context)
        for i in range(len(params)):
            res = param_names[i]
            if res[0] == "func":
                raise Exception("Attempted to assign to funtion")
            temp_context[res[1]] = evaluate_expr(params[i], context)
        return evaluate_expr(expr, temp_context)
    
    elif tree[0] == "a_func":
        if tree[1][0] != "params":
            raise Exception("Attempted to invalid anonymous function")
        param_names = tree[1][1];
        eval_names = []
        for i in param_names:
            res = evaluate_expr(i, context)
            if res[0] == "func":
                raise Exception("Attempted to assign to funtion")
            eval_names.append(res)
        return ("func", eval_names, tree[2])
    
    elif tree[0] == "cond":
        cond = tree[1]
        res = evaluate_expr(cond, context)
        if res[0] == "func":
            raise Exception("Attempted to compare to a function")
        if res[1] <= 0:
            return evaluate_expr(tree[2], context)
        else:
            return evaluate_expr(tree[3], context)
        
    elif tree[0] in "+-/*%&|":
        res1 = evaluate_expr(tree[1], context)
        res2 = evaluate_expr(tree[2], context)
        if res1[0] == "func" or res2[0] == "func":
            raise Exception("Attempted to execute a function")
        res1 = res1[1]
        res2 = res2[1]
        res = None
        if tree[0] == "+":
            res = res1 + res2
        elif tree[0] == "-":
            res = res1 - res2
        elif tree[0] == "/":
            res = res1 // res2
        elif tree[0] == "*":
            res = res1 * res2
        elif tree[0] == "%":
            res = res1 % res2
        elif tree[0] == "&":
            res = res1 & res2
        elif tree[0] == "|":
            res = res1 | res2
        return evaluate_expr(("int", res), context)
    
    elif tree[0] == "neg":
        res = evaluate_expr(tree[1], context)
        if res[0] == "func":
            raise Exception("Attempted to execute a function")
        return evaluate_expr(("int", -res[1]), context)
    
    elif tree[0] == "int":
        if tree[1] in context.keys():
            val = context[tree[1]]
            if val[0] == "int" or val[0] == "intf":
                return evaluate_expr(val, context)
            else:
                return val
        else:
            return ("int", tree[1])
        
    elif tree[0] == "intf":
        return evaluate_expr(tree[1], context)

filename = "input.m1"
if (len(sys.argv) >= 2):
    filename = sys.argv[1]
code = open(filename, "rb")
text = code.read().decode("utf-8")
code.close()
tokenised_code = tokenise(text)
print("Tokens: ", tokenised_code)
tree_code = syntax_tree(tokenised_code, "file")
print("Tree: ", tree_code)
print("--==EXECUTING==--")
output, context = execute(tree_code)
print("--==FINISHED==--")
print(context)
output_file = open("output.txt", "w")
output_file.write(output)
output_file.close()
