Problem Description and Solution

We are asked to write a program that produces the related input file’s llvm code. In other words, we are supposed to write a simple compiler.

We should write a program that reads the input file line by line and after some operations converts this file into llvm code only if there is no error. Hence, I used a while loop as a main loop of the program. Each line goes into loop until all the lines are processed. First, each expression is checked whether there exist any error. I categorized the expressions into two group. The expressions that include assignment and the ones about printing. If there is no error in the expression, it goes to next level. If the expression is an assignment, expression is divided into two parts. The former is the name of the variable and latter is the value of the variable. I take the variable and its value and store them in the hashmap. The calculation of the right hand side of the expression becomes easier if it is converted to postfix. Therefore, I evaluate the right hand side after converting it to postfix.

If the expression is just not an assignment, I calculate the expression first (by using postfix method) and print the right command. After each line process, line number increases by one.

There are five main commands in the llvm code: alloca, store, load, operations(mul, sum, sdiv, sub) and call. While reading the input file, if we encounter a variable on the left side we have to allocate a memory and store the right hand side value in the variable. Therefore, if the line is an assignment we have to write “alloc” and “store” commands in the llvm code. While calculating the right hand side, if we encounter a variable, we have to load its value and write “load” command, and if there is an binary operation we have to do operations and write “add”, “mul”, “sub” or “sdiv” commands.

Software Architecture

isNumber
Takes a string as a parameter, checks each character whether it is non-number character. If it is, returns false otherwise returns true.

isOperator
Takes a char as a parameter. There is an array inside the method which holds +,-,*,/,(,). If the array contains the received character, returns true.

isBinOperator
Slightly different from isOperator method. Distinctly, it doesn’t checks for parenthesis.

hasOperatorError
This methods checks the expression whether it contains extra operator. First, it erases all the spaces.
If expression doesn’t contain any operator, returns false. Then, if the first element or the last element of the expression is a binary operator, or first element of the expression is ‘)’ or the last element is ‘(‘, returns true. In the loop, it looks for any consecutive binary operator, or any binary operator before ‘(’ or after ‘)’.
If this method returns true, program writes “extra operator” and exits.

hasParError
If the received expression doesn’t include parenthesis, returns false. I used a character stack for in order to check if parentheses match. In the for loop, it tracks all the characters in the expression from left to right. If it sees a ‘(‘ it puts it into stack, and pops from the stack if it sees a ’)’. If it tries to pop from the empty stack which means there is no ’(‘ in the stack it returns true.
Program says “parenthesis mismatch” when the return value is true.
hasMisOpError
Briefly looks for any <variable><space><variable>, <variable><space><number>, <number><space><variable>, <number><space><number> error. It tokenizes the given string,
looks all the consecutive tokens. If both of the successive tokens do not contain operators or “=” returns true.
Program says “missing operator” when the function returns true.

equalSignError
Splits the string into pieces according to the equal sign and puts the pieces into an array. If array’s length is greater than 2 which means there is multiple equal signs in the expression returns true.
If the return value is true, program says “multiple ‘=’” and exits.

assignmentError
Returns true, if any side of the equal sign is empty.
Program says “invalid assignment” when this function returns true.

infixToPostfix
This function doesn’t just convert infix expressions to postfix but also it considers the precedence of operators.
For the converted version ‘postfix’ is used. Infix expression is tokenized, and each token is examined. If the first character of the token is not an operator just added to the postfix. For the case that token is a operator, the stack is checked whether there exist any operator with higher precedence, if it does all the operators with higher precedence popped and added to postfix. If the token is right parenthesis, all the operators are popped till the left parentheses and added to postfix.
Finally the function returns postfix.

lowerPrecedence
Takes two characters as parameters op1 and op2 and returns a boolean. If op1 is ‘+’ or ‘–’ and op2 is different from those returns true meaning op1 has lower precedence than op2. If op1 is * or / and op 2 is ‘(‘ again returns true.

calculate
This function calculates the value of a postfix expression. Also do some error check and adds the load command into the code if it sees a variable. There are two integer stacks. One for the numbers or values in other words, the other one is the line numbers in llvm code. Since, after load command we use the line number of the load command in binary operation, line numbers should be stored. Again expression is tokenized. Inside the loop each token is taken from the string. If the token is a binary operator it means that we have two numbers in the stack. So we took two numbers from the stack and also the line numbers and send them to binaryOp function to get the result. Then result is pushed to stack and also the line number. If the token is not an operator but a variable the value of the variable is taken from the hashmap and pushed to stack again. Line number is increased since the load command will be written. If the token is a number, it simply pushed to stack and 0 is pushed to lineNumberStack. 0 means here we are not getting the value of a variable but a number.
This process goes on till the last token. Each time two numbers are taken and the result is pushed. At the end, result returns if the expression isn’t null.

binaryOp
Takes a operator and four numbers. First two are for the operation and the other two for the llvm command. ‘line1’ refers to line number of ‘num1’ and ‘line’ refers to line number of ‘num’. It does the same thing for all operators. If line number is 0, it uses the number in the code, if it is different from 0 it uses the line number. Calculates the the result and returns it back.

printVariable
This function is used for writing the print command into the code. Before the command, first it evaluates the expression. If the expression is unchanged which means expression was just a number, number is added to the print command, if it is changed line number is added to the command.


