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
  - [Section 1: ]

## Section 1: The Principles behind 0cam1
0cam1 is designed with one core aim, and one core principle. Understanding these will make understanding the way the language functions much easier. Firstly, 0cam1 aims to give programmers the neat simplicity of functional programming, whilst giving them the power of mutability. Secondly, 0cam1 is as lazy as possible: values are only updated when they are absolutely needed. 

## Section 2: Base Syntax
In this section we will cover the basic syntax of 0cam1. 

### 1.1 - Basic rules
0cam1 does not rely on formatting as part of its syntax. Instead, it uses commas to separate different lines of code. Each line can either be an assignment, or an expression which is automatically evaluated and outputted, similarly to as follows:
```
1, 2, 3 = 4,
```
Now let's understand basic assignment. 
<br>
<br>
<br>

### 1.2 - Basic Assignment
Assignments are done in 0cam1 by `=`. When the line is executed, the left hand side is evaluated, and is set to hold the expression in the right hand side, as shown by the following:
```
1 = 2, 2 = 3 + 3,
```
We can see the results of our assignments by writing expressions to evaluate the results:
```
1 = 2, 2 = 3 + 3,
1, 2, 3,
```
Has the following output:
```
6, 6, 3
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
### 1.3 Evaluation in 0cam1
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
