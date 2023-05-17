# Welcome to the world of 0cam1
A "functional" esolang with mutable numbers. To use this interpreter run the following command in an adequate command prompt:
```
py 0cam1.py name_of_file.m1
```
The file extension doesn't necessarily need to be .m1, for example you could use a .69420, .txt, or .py.
A condensed partial code is put into code.m1, the output into output.txt, and any errors into errors.txt. These can be overwritten by the second, third and fourth arguments respectively. 

The code formatting rules are vaguely similar to those of ML, but only vaguely. 
This is part of the 69420 class of languages, with the original available here: https://github.com/ProgrammerByte/69420
0cam1's official full name is 69420cam1, but for the sake of brevity the shortened version shall be the primary one in use

> **__NOTE:__** All code examples assume no prior assignment. Be aware that the assignment of values will significantly impact the result of the program. Throughout the guide, `'1'` will be the notation used to represent numerical names. 

## Table of Contents
 - [Welcome to the world of 0cam1](#Welcome-to-the-world-of-0cam1)
  - [Table-of-Contents](#table-of-contents)
  - [Section 1: The Principles behind 0cam1](#section-1-the-principles-behind-0cam1)
  - [Section 2: Basic Syntax](#section-2-basic-syntax)
    - [2.1 - Basic Rules](#21---basic-rules)
    - [2.2 - Comments](#22---comments)
    - [2.3 - Basic Expressions](#23---basic-expressions)
    - [2.4 - Basic Assignment](#24---basic-assignment)
    - [2.5 - Evaluation in 0cam1](#25---evaluation-in-0cam1)
    - [2.6 - Name Evaluation](#26---name-evaluation)
    - [2.7 - Functions](#27---functions)
  - [Section 3: Intermediate Structures](#section-3-intermediate-structures)
    - [3.1 - Conditional Execution](#31---conditional-execution)
    - [3.2 - Anonymous Functions](#32---anonymous-functions)
    - [3.3 - Trivialisation](#33---trivialisation)
    - [3.4 - Random Numbers](#34---random-numbers)
    - [3.5 - Unit](#35---unit)
  - [Section 4: Advanced Structures](#section-4-advanced-structures)
    - [4.1 - Types](#41---types)
    - [4.2 - Pattern Matching](#42---pattern-matching)
    - [4.3 - Strict Evaluation](#43---strict-evaluation)
    - [4.4 - Lists](#44---lists)
    - [4.5 - Character Output](#45---character-output)
    - [4.6 - Integer Input](#46---integer-input)
    - [4.7 - Temporary Assignments and Side Effects](#47---temporary-assignments-and-side-effects)
    - [4.8 - Function Operators](#48---function-operators)
  - [Section 5: Example Code](#section-5-example-code)
    - [5.1 - FizzBuzz](#51---fizzbuzz)
    - [5.2 - Decimal to Binary Converter](#52---decimal-to-binary-converter)
    - [5.3 - Bubblesort](#53---bubblesort)
    - [5.4 - Mergesort](#54---mergesort)

## Section 1: The Principles behind 0cam1
0cam1 is designed with one core aim, and one core principle. Understanding these will make understanding the way the language functions much easier. Firstly, 0cam1 aims to give programmers the neat simplicity of functional programming, whilst giving them the power of mutability. Secondly, 0cam1 is as lazy as possible: values are only updated when they are absolutely needed. 0cam1 is also designed to be as logically consist and robust as possible, with all possible types being treated as equally as possible. Additionally, anything that does not have a return type is accessed through assignments, representing the fact that it does not return anything. 

<br>
<br>

## Section 2: Basic Syntax
In this section we will cover the basic syntax of 0cam1. 

### 2.1 - Basic Rules
0cam1 does not rely on formatting as part of its syntax. Instead, it uses commas to separate different lines of code. Each line can either be an assignment, or an expression which is automatically evaluated and outputted, similarly to as follows:
```
1, 2, 3 = 4,
```
If variable names are integers, then how are character treated? Well, they are treated as...
<br>
<br>

### 2.2 - Comments
0cam1 ignores all characters which are not explicitly used by the language. This means that comments can easily be written using characters no used by 0cam1, which includes all latin letters. The following is an example of valid code using comments:
```
one19nine =equals 2twenty1one This is valid code and is equivalent to, 19=21,  
```
<br>
<br>

### 2.3 - Basic Expressions
0cam1 supports a variety of integer operations, including addition via `+`, multiplication via `*`, subtraction via `-`, integer division via `/`, backwards integer division via `\`, modulo via `%`, bitwise and via `&`, and bitwise or via `|`. Brackets are also supported by 0cam1.
Now let's understand basic assignment. 
<br>
<br>

### 2.4 - Basic Assignment
Assignments are done in 0cam1 by `=`. When the line is executed, the left hand side is evaluated, and is set to hold the expression in the right hand side, as shown by the following:
```
1 = 2, 2 = 3 + 3, (4 + 4) = 7,
```
We can see the results of our assignments by writing expressions to evaluate the results:
```
1 = 2, 2 = 3 + 3, (4 + 4) = 7,
1, 2, 3, 8,
```
Has the following output:
```
6
6
3
7
```
This makes sense, `'1'` has the expression `2` assigned to it, and `'2'` has the expression `3 + 3` assigned to it, whilst `'3'` has not been altered. Therefore, when evaluating `1`, it evaluates the expression `2`. which evaluates to `3 + 3`, ultimately giving out answer of `6`. 

These can easily combine in more complex expressions:
```
1 = 2, 2 = 3 + 3,
1 + 2 + 3,
```
Has the following output:
```
15
```
Note that care must be taken to avoid creating infinite loops. The line `1=1, 1,` will never terminate. 
<br>
<br>

### 2.5 - Evaluation in 0cam1
If we try the example
```
3 = 5,
3 + 2 + 1
```
we get the output
```
10
```
This may be surprising, but this is because 0cam1 has to evaluate the true value of every integer after every calculation step. 0cam1 follows (B)(O)(DM)(AS) rules, and applies the right most operator first, so the order of operations on `3 + 2 + 1` is `3 + (2 + 1)`. When evaluating this expression, it first evaluates to `3 + (3)`, which evaluates to `5 + 5`, yielding `10`. Note that this breaks the associativity of operations: in this context `1 + 2 + 3` evaluates to `1 + (2 + 5) = 1 + 7 = 8`.
<br>
<br>

### 2.6 - Name Evaluation
Names in 0cam1 are evaluated slightly differently to standard expressions. If a direct integer is given for a name, the direct integer is returned. Otherwise the expression is evaluateed. Names must always evaluate to an integer. Note that brackets can be used to force evaluation. Name evaluation is used for variable names, function names and paramters, type names and parameters, and values being trivialised. This behaviour is demonstrated by the following code:
```
3 = 4, (3) = 7, 3 = 6, 
3, 4
```
Which evaluates to:
```
6
7
```
<br>
<br>

### 2.7 - Functions
Having established how to assign integer values, we now move to creating functions. Functions are created in a very similar way to assigning integer values, simply by using `=` to set the function handle to the function's expression. Functions can have integer parameter names, including expressions. These are evaluated and consolidated once the function is created; once the function handle has been evaluated the function and parameter names will stay the same regardless of what happens to their underlying values. 

Let's make some simple functions to see how 0cam1 works. 
```
123 124 = 124 + 1,
125 124 126 = 124 + 126,
123 5, 125 4 5, 123 (125 1 2), 123 (2 - 1), 125 (0 - 1) 1,
```
Evaluates to
```
6
9
4
2
0
```
Note that when returned, 0cam1 automatically prints them as a list of parameters, followed by `>`, followed by a rough expression of what the function equals, as shown by:
```
123 124 = 124 + 1,
125 124 126 = 124 + 126,
123, 125
```
Returning:
```
124 > 124+1
124 126 > 124+126
```
Like most functional programming languages, 0cam1 supports first class functions, currying, and passing around functions as arguments. Note that curried arguments are still evaluated lazily when called rather than when saved. This is demonstrated by the following simple examples:
```
99 100 101 = 100 + 101,
40 42 43 = 42 43,
30 = 99 10,
40 (99 5) 4,
30 5,
10 = 2,
30 5,
```
Evaluates to
```
9
15
7
```
This so far is not too useful, but with a few additional structures which we will look at now, mildly useful 0cam1 programs can be made. 
<br>
<br>

## Section 3: Intermediate Structures
In this section we will cover the more advanced structures used to make useful 0cam1 programs. 

### 3.1 - Conditional Execution
0cam1 performs branches using the `? :` operator. This takes three variables, the condition `c`, the less than or equal to value `l`, and the greater than value `g`, in the format `c ? l : g`. If `c<=0`, then the branch returns `l`, otherwise it returns `g`. We can chain these together to produce more complex behaviours, such as the following:
```
997 998 999 = (999 - 998) ? (998 - 999 ? 1 : 0) : 0, This is an equality function, if nine nine eight equals nine nine nine, then it returns one, otherwise it returns zero
997 2 2,
997 0 2,
997 2 0,
```
Which evaluates to:
```
1
0
0
```
Like in most functional languages, combining conditional branches with recursion allows for the creation of loops. This opens the door to a significant number of programs, such as the following:
```
9997 9998 = 9998 + 1 ? 0 : 9998 + 9997 (9998 - 1),                                   A function to calculate triangular numbers
16180 33988 = 33988 ? 0 : 33988 - 1 ? 1 : (16180 (33988 - 1)) + (16180 (33988 - 2)), A function to calculate the Fibonacci numbers
9997 14,
16180 10,
```
Which outputs:
```
105
55
```
This can combine with first class functions to produce the following:
```
9996 9997 9998 9999 = 9998 ? 9999 : 9997 (9996 9997 (9998 - 1) 9999), Applies a function n times to an initial value x
10001 10002 = 10002 + 1,                                              Creates a successor function
10003 10004 10005 = 9996 10001 10004 10005,                           Creates an addition function from repeated succession
10006 10007 10008 = 9996 (10003 10007) 10008 0,                       Creates a multiplication function from repeated addition
10009 10010 10011 = 9996 (10006 10010) 10011 1,                       Creates an exponentiation function from repeated multiplication
10003 2 5,
10006 2 5,
10009 2 5,
```
Which evaluates to:
```
7
10
32
```
<br>
<br>

### 3.2 - Anonymous Functions
0cam1 supports anonymous functions through the `>` operator. The syntax is exactly the same as assigning a named function, however the function name is not required. Since anonymous functions and their names are only evaluated when the function is needed, anonymous functions feature lazy name evaluation, which can have interesting use cases. Here is some example code that uses anonymous functions to check if a given value is one:
```
9990 9991 = ((9991 - 1) > 0) 9991, Since the parameter name is evaluate once the functions parameter is passed in the name can be zero if the input is one which alters the returned value
9990 1,
9990 0,
9990 2,
```
Which gives the output:
```
1
0
0
```
<br>
<br>

### 3.3 - Trivialisation
What happens when we want to reset a value to its value before any assignments? The answer is we can use trivialisation to trivially reset a name to its trivial value. The trivialisation namespace is trivially the empty set. Assigning to trivialisation trivially trivialises the name, and can be trivially done with multiple names are once, such as in the following code:
```
1 = 2, 2 = 3, 3 = 4, 5 = 7, 6 = 8, 4 = 9, Made a bit of a mess, and want to clear it up
1, 2, 3, 4, 5, 6,                         Pre trivialisation
{} = 1 3 5,                               Trivialisation
1, 2, 3, 4, 5, 6,                         Post trivialisation
```
Trivially returning:
```
9
9
9
9
7
8
1
3
3
9
5
8
```
Note that the names provided by trivialisation are evaluated like all names in 0cam1; if a direct value is given it is used without further evaluation, otherwise the expression is evaluated. 
<br>
<br>

### 3.4 - Random Numbers
0cam1 features the inbuilt `??` function for generating random numbers. It can be called with either 0, 1, or 2 parameters. When called with 0 parameters, it returns a random integer from 0 to 1. When called with 1 parameter, it returns a random integer from 0 to the first parameter. When called with 2 parameters, it returns a random integer between the two parameters. Here is an example:
```
??, ?? 100, ?? -100 (-10),
```
Could evaluate to:
```
1
64
-72
```
Note that this can be used for random name assignment, as with the following:
```
?? = 5, 0, 1
```
Which could evalute to:
```
0
5
```
<br>
<br>

### 3.5 - Unit
Sometimes we want to have a dummy object that has no inherent meaning. To achieve this we use `()`, aka unit. `()` can be used for parameter names, and has the effect of discarding the parameter by not assigning it into the namespace. `()` can also be used as an input when no input is required. Additionally, `()` combined with anything else by an operator returns `()`, `()` returns `()` when called as a function with anything, `()` returns `()` when compared, `()` returns `()` if it fails a pattern match, and `()` will print `()` when converted to a string. This is all shown by the following:
```
5 () = 3, 5 2, 5 (), () + 2, () + 5, () 1 2, () ? 1 : 2, () ! 1 > 2, $ = (),
```
Printing:
```
3
3
()
()
()
()
()
()
```
<br>
<br>

## Section 4: Advanced Structures
In this section, we'll cover the most advanced 0cam1 structures. 
### 4.1 - Types
0cam1 supports types. To create a type, assign to \_, akin to the following:
```
_ = 123 ! 124 125 126,
```
When types are returned, 0cam1 prints them as a list of their parameter names, followed by an !, as shown by the following:
```
_ = 123 ! 124 125 126,
123, 124,
```
Which outputs:
```
123 
125 126 !
```
Note the use of `!` to separate different constructors for the same type. 
This creates the constructors `123` and `124`. We can then instantiate this type using the constructors. For example:
```
_ = 123 ! 124 125 126,
123, 124 5 (124 6 123), 3 = 123, 124 2 3,
```
Evaluates to:
```
123 
124 5 124 6 123
124 2 3
```
This shows how 0cam1 returns constructed objects, as their constructor, followed by their parameters roughly as expressions. This also shows 0cam1's lazy evaluation, since `3` is not evaluated to `123` until it is needed.
Partial constructor calls are also possible, and return a new type, such as in the following:
```
_ = 123 ! 124 125 126,
124 5, (124 5) 123,
```
Which returns:
```
126 !
124 5 123
```
We may wonder what are types useful for, since we currently cannot manipulate them. To fix this, we add...
<br>
<br>

### 4.2 - Pattern Matching
Pattern matching allows us to usefully check what types our values have, and extract their constructor values. The pattern matching is done using `!`, which also acts as the separator between the various statements: the first statement is the value being comapred to, the rest are match cases. A match case consists of a thing to match, followed by `>` and the expression to return if the case is matched. Pattern matching matches types, matching the constructors, and passed in values. For example, if we have a type `_ = 7331 23 24`, then `(7331 1 2)  ! 7331 1 > 0 ! 7331 > 2` returns `0`, and `(7331 2 2)  ! 7331 1 > 0 ! 7331 > 2` returns `2`. In order to access the parameters passed ot the constructors, unmatched parameters are written into the match's context using the constructor's parameter names. So `(7331 1 2)  ! 7331 1 > 23 ! 7331 > 23` returns `23` since the `1` is matched, and `(7331 2 2)  ! 7331 1 > 23 ! 7331 > 23` returns `2` since the `2` is not. This allows us to make some brief full example code:
```
_ = 123 124 125! 236,
997 998 = 998 ! 236 > 0 ! 123 > 1 + 997 125,
997 236, 997 (123 5 (123 6 236)),
```
Which gives:
```
0
2
```
<br>
<br>

### 4.3 - Strict Evaluation
We may notice that constructors in 0cam1 have a problem, namely that they are by default lazy. This presents an issue, where objects constructed within a scope can lose all meaning once passed out of the scope. To fix this we can use the strict evaluation operators `!?` and `!!`. `!?` is shallow strict evaluation, it strictly evaluates the given value, but if the value has a constructor in it, the constructor's arguments are not evaluated. `!!` is deep strict evaluation, all of the nested constructors within are evaluated. These can also be used for regular assignments, as shown by the following code:
```
_ = 10011 10012,10011 (* ((10011 (1 + 2)) + (10011 (-(4 + []))) + [])),
10011 (!?(* ((10011 (1 + 2)) + (10011 (-(4 + []))) + []))),
10011 (!!(* ((10011 (1 + 2)) + (10011 (-(4 + []))) + []))),
3 = !? (12 + (13 + 2)), 3,
3 = !! (12 + (13 + 3)), 3,
```
Which returns:
```
10011 *((10011 (1+2)+(10011 -((4+[]))+[])))
10011 10011 (1+2)
10011 10011 3
27
52
```
<br>
<br>

### 4.4 - Lists
0cam1 has an inbuilt list type. It has two associated constructors, `+` and `[]`. `[]` returns the empty list, and `h+t` conses `h` to `t`. This means that we can easily build lists as shown by the following:
```
1 + 2 + 3 + [],
```
Returning:
```
[1, 2, 3]
```
Note that lists can contain anything, from other lists to functions. 
The `-` operator is used to get the tail of a list, whilst the `*` operator is used to get the head. These can be chained, as shown by:
```
1234 = 1 + 2 + 3 + 4 + [],
-1234, *1234, ---(1234), *--(1234),
```
Resulting in:
```
-1234
1
[4]
3
```
We can pattern match with lists as with any other data type, allowing us to rewrite our length function from earlier as:
```
997 998 = 998 ! [] > 0 ! + > 1 + 997 (-(998)),
997 [], 997 (1 + 2 + 3 + []), +,
```
Which gives:
```
0
3
() () !
```
Note that `+`'s two parameters are units, and therefore do not alter the namespace when matched to. 
<br>
<br>

### 4.5 - Character Output
We can output characters by writing to `$`. Like `{}`, `$` can be assigned to any number of values, which are evaluated, converted to strings, conctenated, and outputted. `$` can automatically convert any integer, and any list structure which ultimately contains only integers. For example:
```
$ = 65,
$ = (72+101+108+108+111+32+87+111+114+108+100+33+[]),
```
Results in:
```
A
Hello World!
```
<br>
<br>

### 4.6 - Integer Input
The function `<` can be used to ask for input. It evaluates to whatever integer is inputed. This is shown by:
```
$ = (73+110+112+117+116+[]),
< + 1, 
```
Returning whatever is inputed + 1, which could result in the output
```
Input
4
5
```
<br>
<br>

### 4.7 - Temporary Assignments and Side Effects
Sometimes we want to temporarily assign values. 0cam1 does this using `.`, which separates the different statements, of which the last must return a value, and the rest will only perform side effects. Any expressions in a side effect statement will merely output its result. When performing temporary assignments, `~` is used instead of `=`. All of the features of `=`, including trivialisation and character output are available through this. All temporary bindings will be lost once the final statement is evaluated. Note tha side effect statements are evaluated in order. This explains how:
```
3 ~ 5. 4 ~ 3 + 5. $ ~ 66. 4. 5. 3, 3
```
Returns with:
```
B
10
5
5
3
```
<br>
<br>

### 4.8 - Function Operators
0cam1 supports combining functions with operators. This produces a new anonymous function which returns the relevant to the two functions, provided it is given all of the required parameters. For example:
```
100 101 = 101 + 1,
102 103 = -(103),
100 + 102, (100 * 102) 4 6, 
```
Which results in:
```
101 103 > 101+1+- 103
-30
```
<br>
<br>

## Section 5: Example Code
This section is dedicated to code showing the power and usefulness of 0cam1. 

### 5.1 - FizzBuzz
```
Print out the final returned string as well
$ = 
Convert a number into a ASCII decimal string
(997 998 999 ~ (998 ? 999 : 997 (998 / 10) ((998 % 10 + 48) + 999)).
FizzBuzz
1007 1009 ~ ((1009 % 3) ? 
((1009 % 5) ?  FizzBuzz 70+105+122+122+66+117+122+122+[] : Fizz 70+105+122+122+[]) : 
(1009 % 5) ? Buzz 66+117+122+122+[] : 997 1009 []).
Iterate FizzBuzz
1013 1017 1019 ~ ((1019 - 1017) ? 1007 1019 : ($ ~ (1007 1017). 1013 (1017 + 1) 1019)).

Ask how many iterations the user wants
$ ~ (72+111+119+32+102+97+114+32+116+111+32+99+111+117+110+116+63+32+[]).
Respond
(1013 1 <)),
```
<br>
<br>

### 5.2 - Decimal to Binary Converter
```
$ = (997 999 998 ~ (998 ? 999 : 997 ((998 % 2 + 48) + 999) (998 / 2)). Converts decimal to binary

Several test cases to show it working
$ ~ (73+110+112+117+116+[]).
(997 [] <)), 
```
<br>
<br>

### 5.3 - Bubblesort
```
Bubblesort
9997 9998 = (
 A single bubble sort pass
 1013 1017 ~ (1017 ! [] > [] ! + > 
  (-(1017) ! [] > 1017 ! + > 
   (*1017 - *(-(1017))) ?  
   *1017 + (1013 (*-(1017) + --(1017))) :
   *(-(1017)) + (1013 (*1017 + --(1017))))
 ).
 Getting the length of the list
 1023 1027 ~ (1027 ! [] > 0 ! + > 1 + (1023 (-(1027)))).
 Repeating the pass a given number of times
 1033 1037 1039 ~ (1039 ? 1037 : 1013 (1033 1037 (1039 - 1))).
 Repeating the pass for the number of items in the list
 1033 9998 (1023 9998)
),
Some test cases to show it works
9997 (1 + 3 + 5 + 4 + 2 + []),
9997 (5 + 4 + 3 + 2 + 1 + []),
9997 (4 + 2 + 3 + 5 + 1 + []),
```
<br>
<br>

### 5.4 - Mergesort
```
Mergesort
9997 9998 = (
  Mergesort
  10001 10002 10003 10007 10011 ~ (
    10002 
     ! [] > (
       10003 
        ! [] > (
         10007
          ! [] > []
          ! + > (
           -(10007)
            ! [] > 10007
            ! + > 10001 10007 [] [] 1
         )
       )! + > (
         10007
          ! [] > (
           -(10003)
            ! [] > 10003
            ! + > 10001 10003 [] [] 1
         )! + >
           Merge sorted split lists
           10201 (10001 10003 [] [] 1) (10001 10007 [] [] 1)
       )
    )
      Split lists
     ! + > ( 10011? 
      10001 (-(10002)) 10003 (*10002 + 10007) 1 :
      10001 (-(10002)) (*10002 + 10003) 10007 (-1)
    )
  ).
  Merge Lists
  10201 10205 10207 ~ (
    10205 
     ! [] > 10207
     ! + > (
      10207
       ! [] > 10205
       ! + >
        (*10205 - *10207) ? 
          *10205 + (10201 (-(10205)) 10207) :
          *10207 + (10201 10205 (-(10207)))
    )
  ).
  10001 9998 [] [] 1
),

Some test cases to demonstrate functionality
9997 (5 + 3 + 4 + 2 + 1 + []),
9997 (1 + 3 + 5 + 4 + 10 + 9 + 6 + 7 + 8 + 2 + []),
9997 (10 + 4 + 6 + 7 + 3 + 2 + 8 + 1 + 5 + 9 +  []),
```
<br>
<br>

### 5.5 - Quicksort
```
Quicksort
9997 9998 = (
  Quicksort
  10001 10002 10003 10007 10011 10013 ~ (
    10002 
     ! [] > (
       10003 
        ! [] > (
         10007
          ! [] > 10013 Return final result
          ! + > (
           -(10007)
            ! [] > *10007 + 10013
            ! + > 10001 10007 [] [] (*10007) 10013
         )
       )! + > (
         10007
          ! [] > (
           -(10003)
            ! [] > *10003 + 10013
            ! + > 10001 10003 [] [] (*10003) 10013
         )! + >
           Sort and combine sub lists
           10001 10003 [] [] (*10003) (10001 10007 [] [] (*10007) 10013)
       )
    )
      Split lists by pivot
     ! + > ( *10002 - 10011 ?
      10001 (-(10002)) (*10002 + 10003) 10007 10011 10013 :
      10001 (-(10002)) 10003 (*10002 + 10007) 10011 10013
    )
  ).
  10001 9998 [] [] (*9998) []
),

Some test cases to demonstrate functionality
9997 (5 + 3 + 4 + 2 + 1 + []),
9997 (1 + 3 + 5 + 4 + 10 + 9 + 6 + 7 + 8 + 2 + []),
9997 (10 + 4 + 6 + 7 + 3 + 2 + 8 + 1 + 5 + 9 +  []),
```
