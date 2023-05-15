# Welcome to the world of 0cam1
A "functional" esolang with mutable numbers. To use this interpreter run the following command in an adequate command prompt:
```
py 0cam1.py name_of_file.m1
```
The file extension doesn't necessarily need to be .m1, for example you could use a .69420, .txt, or .py.

The code formatting rules are vaguely similar to those of ML, but only vaguely. 
This is part of the 69420 class of languages, with the original available here: https://github.com/ProgrammerByte/69420
0cam1's official full name is 69420cam1, but for the sake of brevity the shortened version shall be the primary one in use

> **__NOTE:__** All code examples assume no prior assignment. Be aware that the assignment of values will significantly impact the result of the program. Throughout the guide, `'1'` will be the notation used to represent numerical names. 

## Table of Contents
  - [Section 1: The Principles behind 0cam1](#section-1-the-principles-behind-0cam1)
  - [Section 2: Basic Syntax](#section-2-basic-syntax)
    - [2.1 - Basic Rules](#21---basic-rules)
    - [2.2 - Comments](#22---comments)
    - [2.3 - Basic Assignment](#23---basic-assignment)

## Section 1: The Principles behind 0cam1
0cam1 is designed with one core aim, and one core principle. Understanding these will make understanding the way the language functions much easier. Firstly, 0cam1 aims to give programmers the neat simplicity of functional programming, whilst giving them the power of mutability. Secondly, 0cam1 is as lazy as possible: values are only updated when they are absolutely needed. 

## Section 2: Basic Syntax
In this section we will cover the basic syntax of 0cam1. 

### 2.1 - Basic Rules
0cam1 does not rely on formatting as part of its syntax. Instead, it uses commas to separate different lines of code. Each line can either be an assignment, or an expression which is automatically evaluated and outputted, similarly to as follows:
```
1, 2, 3 = 4,
```
Now let's understand basic assignment. 
<br>
<br>
<br>

### 2.2 - Comments
0cam1 ignores all characters which are not explicitly used by the language. This means that comments can easily be written using characters no used by 0cam1, which includes all latin letters. The following is an example of valid code using comments:
```
one1 =equals 2twenty0 This is valid code and is equivalent to, 1=20,  
```
<br>
<br>
<br>

### 2.3 - Basic Expressions
0cam1 supports a variety of integer operations, including addition via `+`, multiplication via `*`, subtraction via `-`, integer division via `/`, modulo via `%`, bitwise and via `&`, and bitwise or via `|`. 

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
6, 6, 3, 7
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
Note that care must be taken to avoid creating infinite loops. The line `1=1` will never terminate. 
<br>
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
This may be surprising, but this is because 0cam1 has to evaluate th1 true value of every integer after every calculation step. 0cam1 follows (B)(O)(DM)(AS) rules, and applies the right most operator first, so the order of operations on `3 + 2 + 1` is `3 + (2 + 1)`. When evaluating this expression, it first evaluates to `3 + (3)`, which evaluates to `5 + 5`, yielding `10`. Note that this breaks the associativity of operations: in this context `1 + 2 + 3` evaluates to `1 + (2 + 5) = 1 + 7 = 8`.
<br>
<br>
<br>

### 2.6 - Functions
Having established how to assign integer values, we now move to creating functions. Functions are created in a very similar way to assigning integer values, simply by using `=` to set the function handle to the function's expression. Functions can have integer parameter names, including expressions. These are evaluated and consolidated once the function is created; once the function handle has been evaluated the function and parameter names will stay the same regardless of what happens to their underlying values. Functions can be called simply by listing out the passed in parameters with whitespace between. 

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
Like most functional programming languages, 0cam1 supports first class functions, currying, and passing around functions as arguments. Note that curried arguments are still evaluated lazily when called rather than when saved. This is demonstrated by the following simple examples:
```
99 100 101 = 100 + 101,
40 42 43 = 42 43,
30 = 99 10,
40 (99 5) 4,
30 5,
```
Evaluates to
```
9
15
```
This so far is not too useful, but with a few additional structures which we will look at now, mildly useful 0cam1 programs can be made. 
<br>
<br>
<br>

## Section 3: Advanced Structures
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
<br>

### 3.3 - Trivialisation
What happens when we want to reset a value to its value before any assignments? The answer is we can use trivialisation to trivially reset a value to its trivial value. The trivialisation function is trivially the empty set, and can be trivially applied to multiple names at once. Trivialisation is the one function that does not trivially evaluate names through the dependency chain, instead clearing the exact name of the given integer. Due to this, trivialisation trivially cannot accept expressions as arguments, and only accepts direct integers, as trivially shown by the following:
```
1 = 2, 2 = 3, 3 = 4, 5 = 7, 6 = 8, 4 = 9, Made a bit of a mess, and want to clear it up
1, 2, 3, 4, 5, 6,                         Pre trivialisation
{} 1 3 5,                                 Trivialisation
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
Due to the fact the trivialisation alters the mappings on the base execution layer, trivialisation is not allowed within functions, and is only valid when on a line by itself. 
<br>
<br>
<br>

### 3.4 - Character Output
Sometimes we may wish to abandon integers for characters. In such rare cases, the character output function `$` can help us, converting integers into their relevant characters, and outputting the result. Note that similar to trivialisation, `$` can receive multiple parameters which are all printed as one string, and is also restricted to use on a line by itself, and not within functions. Here is some basic code using `$`:
```
$ 65, $ 66 67,
```
Which prints:
```
A
BC
```

### Section 4: Example Code
This section is dedicated to code showing the power and usefulness of 0cam1. 
