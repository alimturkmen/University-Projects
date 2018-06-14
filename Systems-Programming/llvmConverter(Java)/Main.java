/**
 * Created by alim
 */

import java.io.*;
import java.util.*;

public class Main {

    public static HashMap<String, Integer> variables = new HashMap<String, Integer>(); // stores the variables with their values

    public static String code = ""; // it is the llvm code
    public static int lineNumber = 0; // line-number in the llvm code
    public static int lineCounter = 1; // line-number in the input file
    public static PrintStream ps; //writes into output file

    //Takes the written statements and converts them into llvm
    //If there any error exists, it prints error and exits
    public static void main (String[] args) throws FileNotFoundException{

        File file = new File(args[0]);
        Scanner input = new Scanner(file);

        //Takes the input file's name without the extension
        int index = args[0].length();
        for(int i=0; i<index; i++){
            if(args[0].charAt(i)=='.'){
                index = i;
                break;
            }
        }
        //Output file's name
        String output = args[0].substring(0, index);

        code += ("; ModuleID = 'stm2ir'\n");
        code += ("declare i32 @printf(i8*, ...)\n");
        code += ("@print.str = constant [4 x i8] c\"%d\\0A\\00\"\n");
        code += ("define i32 @main() {\n");

        //Main loop of the program
        //Reads the input file line by line and produces the related llvm code
        while(input.hasNextLine()){
            //expression in each line
            String expression = input.nextLine();
            if(hasOperatorError(expression)){
                System.out.println("Error: Line "+lineCounter+": extra operator");
                System.exit(0);
            }
            if(hasParError(expression)){
                System.out.println("Error: Line "+lineCounter+": missing paranthesis");
                System.exit(0);
            }
            if(hasMisOpError(expression)){
                System.out.println("Error: Line "+lineCounter+": missing operator");
                System.exit(0);
            }
            if(equalSignError(expression)){
                System.out.println("Error: Line "+lineCounter+": multiple '=' ");
                System.exit(0);
            }
            if(assignmentError(expression)){
                System.out.println("Error: Line "+lineCounter+": invalid assignment");
                System.exit(0);
            }

            if(expression.contains("=")){
                String [] array = expression.split("=");
                String var = array[0]; //variable in the expression
                var = var.replaceAll(" ", "");
                if(!variables.containsKey(var)) {
                    code += (" %" + var + " = alloca i32\n");
                }
                expression = array[1];
                expression = infixToPostfix(expression);
                int value = calculate(expression); //integer value of the expression
                variables.put(var, value);
                array[1] = array[1].replace(" ", "");
                if(array[1].equals(Integer.toString(value))) {
                    code += (" store i32 " + value + ", i32* %" + var +"\n");
                }else{ code += (" store i32 %" + lineNumber + ", i32* %" + var +"\n");}
            }else
                printVariable(expression);
            lineCounter++;
        }
        code += (" ret i32 0 \n}\n");
        ps = new PrintStream(output+".ll");
        ps. print(code);
    }

    //Tells whether token is a number or not
    //Looks all the characters in token and checks whether there is a non-number character
    public static boolean isNumber(String token){
        char [] numArray = {'0','1','2','3','4','5','6','7','8','9'};
        for(int i=0; i<token.length(); i++){
            int counter=0;
            for(int j=0; j<numArray.length; j++){
                if(token.charAt(i)==numArray[j])
                    break;
                else counter++;
            }
            if(counter==10)
                return false;
        }
        return true;
    }

    // Tells whether c is an operator or not ( +, -, *, /, (, ) )
    public static boolean isOperator(char c) {
        char [] opArray = {'+','-','*','/','(',')'};
        for(int i=0; i<6;i++){
            if(opArray[i]==c)
                return true;
        }
        return false;
    }

    //Tells whether c is a binary operator or not ( +, -, *, / )
    public static boolean isBinOperator(char c) { // Tell whether c is an operator.
        return (c=='+' || c=='-' || c=='*' || c=='/' );
    }

    //Tells whether any extra operator is used or not in expr
    //Any consecutive operators (including '(', ')') counted as an error
    //Any invalid usage of operators counted as an error
    public static boolean hasOperatorError(String expr){
        expr = expr.replaceAll(" ", "");
        if(!expr.contains("+") && !expr.contains("-") && !expr.contains("*") && !expr.contains("/")
                && !expr.contains("(") && !expr.contains(")"))
            return false;
        if(isBinOperator(expr.charAt(0)) || isBinOperator(expr.charAt(expr.length()-1) ))
            return true;
        if(expr.length()>1 && ((expr.charAt(0) == '(' && expr.charAt(1)==')' ) ||
                (expr.charAt(expr.length()-1) == ')' && expr.charAt(expr.length()-2)=='(' )))
            return true;
        if(expr.charAt(0)==')' || expr.charAt(expr.length()-1)=='(')
            return true;
        for(int i=1; i<expr.length()-1; i++) {
            if(isBinOperator(expr.charAt(i)) && (isBinOperator(expr.charAt(i+1)) ||
                    expr.charAt(i+1)==')' || expr.charAt(i-1)=='('))
                return true;
            else if(expr.charAt(i) == '(' && expr.charAt(i+1)==')')
                return true;
            else if(expr.charAt(i) == ')' && expr.charAt(i+1)=='(')
                return true;
        }
        return false;
    }

    //Tells whether any error about parenthesis exist in expr
    //If expression doesn't have any parenthesis it returns false meaning no error
    //Stores '('s in a stack, whenever catches a ')' pops one of '('s out
    //At the end if any '(' remains, returns true, otherwise returns false
    public static boolean hasParError(String expr){
        if(!expr.contains("(") && !expr.contains(")"))
            return false;
        Stack<Character> parStack = new Stack<Character>();
        for(int i=0; i<expr.length(); i++) {
            if (expr.charAt(i) == '(') {
                parStack.push('(');
            } else if (expr.charAt(i) == ')') {
                if(parStack.isEmpty())
                    return true;
                parStack.pop();
            }
        }
        return !parStack.isEmpty();
    }

    // Tells whether any consecutive numbers, or variables exist in expr
    public static boolean hasMisOpError(String expr) {
        StringTokenizer tokens = new StringTokenizer(expr);
        String token1,token2;
        if(tokens.hasMoreTokens())
            token1 = tokens.nextToken();
        else return false;
        if(tokens.hasMoreTokens())
            token2 = tokens.nextToken();
        else return false;
        if( (isNumber(token1) || (!isOperator(token1.charAt(0)) && !isOperator(token1.charAt(token1.length()-1)) && !token1.contains("="))) &&
                (isNumber(token2) || (!isOperator(token2.charAt(0)) && !isOperator(token2.charAt(token2.length()-1)) &&!token2.contains("="))) )
            return true;
        while(tokens.hasMoreTokens()) {
            token1 = token2;
            token2 = tokens.nextToken();
            if( (isNumber(token1) || (!isOperator(token1.charAt(0)) && !isOperator(token1.charAt(token1.length()-1)) && !token1.contains("="))) &&
                    (isNumber(token2) || (!isOperator(token2.charAt(0)) && !isOperator(token2.charAt(token2.length()-1)) &&!token2.contains("="))) )
                return true;
        }
        return false;
    }

    //Tells whether multiple '=' is used or not in expr
    public static boolean equalSignError(String expr){
        String [] arr = expr.split("=");
        if(arr.length>2)
            return true;
        return false;
    }

    //Tells whether the assignment in the given expression is valid or not
    public static boolean assignmentError(String expr) {
        if(!expr.contains("="))
            return false;
        String [] arr = expr.split("=");
        if(arr.length<2) return true;
        if(arr[1].replaceAll(" ","").equals("")) return true;
        if(arr[0].replaceAll(" ","").equals("" ))return true;
        return false;
    }

    //Converts the given infix expression into postfix expression and returns it
    public static String infixToPostfix(String infix) {
        Stack<String> operators = new Stack<String>();
        char c;
        StringTokenizer tokenizer = new StringTokenizer(infix,"+-*/() ",true);
        String postfix = "";
        while (tokenizer.hasMoreTokens()) {
            String token = tokenizer.nextToken();
            c = token.charAt(0);
            if ( (token.length() == 1) && isOperator(c) ) {
                while (!operators.empty() && !lowerPrecedence(operators.peek().charAt(0), c)) {
                    postfix = postfix + " " + operators.pop();
                }
                if (c==')') {
                    String operator = operators.pop();
                    while (operator.charAt(0)!='(') {
                        postfix = postfix + " " + operator;
                        operator = operators.pop();
                    }
                }
                else
                    operators.push(token);
            }
            else if ( c!=' ') { postfix = postfix + " " + token;
            }
        }
        while (!operators.empty())
            postfix = postfix + " " + operators.pop();

        return postfix;
    }

    //Tells whether op1 has lower precedence or not.
    // +,-,*,/ are the operators that are checked,
    // '(' is the character for the precedence of parenthesis
    public static boolean lowerPrecedence(char op1, char op2) {
        if( (op1=='+' || op1=='-') && !(op2=='+' || op2=='-')){ // +,-  <  *, /, (
            return true;
        }else if( (op1=='*' || op1=='/') && (op2=='(') ){ // *,/ <  (
            return true;
        }else if( op1 == '('){
            return true;
        }else { return false; }

    }

    //Calculates the given postfix expression and returns the result
    public static int calculate(String expr){
        Stack<Integer> stack = new Stack<Integer>(); // Stores the each operations result
        Stack<Integer> lineNumberStack = new Stack<Integer>(); // Stores the line number in the llvm code
        //num1, num2 are the first two numbers that are encountered
        //ln1, ln2 are the line numbers of the first two values
        //result is the final result
        int num1, num2, ln1, ln2, result = 0;
        StringTokenizer tokenizer = new StringTokenizer(expr);
        String token;
        while (tokenizer.hasMoreTokens()) {
            token = tokenizer.nextToken();
            char c = token.charAt(0);
            if (isOperator(c)) {
                num2 = stack.pop();
                num1 = stack.pop();
                ln2 = lineNumberStack.pop();
                ln1 = lineNumberStack.pop();
                result = binaryOp(token.charAt(0), num1, num2, ln1, ln2);
                stack.push(result);
                lineNumberStack.push(lineNumber);
            }
            else if(variables.keySet().contains(token)){
                stack.push(variables.get(token));
                lineNumber++;
                lineNumberStack.push(lineNumber);
                code += (" %"+lineNumber+" = load i32* %"+token+ "\n");
            }else if(!isNumber(token)){
                lineNumber++;
                System.out.println("Error: Line "+lineCounter+": undefined variable "+token);
                System.exit(0);
            }
            else {
                stack.push(Integer.valueOf(token));
                lineNumberStack.push(0);
            }
        }
        if(!stack.isEmpty())
            result = stack.pop();
        return result;
    }

    //Does the binary operations (summation, subtraction, division, or multiplication)
    //Writes the correct command into the llvm code
    // num1 and num2 are the numbers, line1 and lin2 are the line numbers respectively
    // operation is the binary operation
    public static int binaryOp(char operation, int num1, int num2, int line1, int line2) {
        if (operation == '+') {
            if(line1==0 && line2==0) {
                lineNumber++;
                code += (" %" + lineNumber + " = add i32 " + num1 + "," + num2 + "\n");
            }else if(line1==0 && line2!=0){
                lineNumber++;
                code += (" %" + lineNumber + " = add i32 " + num1 + ",%" + line2+ "\n");
            }else if(line1!=0 && line2==0){
                lineNumber++;
                code += (" %" + lineNumber + " = add i32 %" + line1 + "," + num2+ "\n");
            }else{
                lineNumber++;
                code += (" %" + lineNumber + " = add i32 %" + line1 + ",%" + line2+ "\n");
            }
            return num1 + num2;

        }else if (operation == '-') {
            if(line1==0 && line2==0) {
                lineNumber++;
                code += (" %" + lineNumber + " = sub i32 " + num1 + "," + num2+ "\n");
            }else if(line1==0 && line2!=0){
                lineNumber++;
                code += (" %" + lineNumber + " = sub i32 " + num1 + ",%" + line2+ "\n");
            }else if(line1!=0 && line2==0){
                lineNumber++;
                code += (" %" + lineNumber + " = sub i32 %" + line1 + "," + num2+ "\n");
            }else{
                lineNumber++;
                code += (" %" + lineNumber + " = sub i32 %" + line1 + ",%" + line2+ "\n");
            }
            return num1 - num2;
        }else if (operation == '*'){
            if(line1==0 && line2==0) {
                lineNumber++;
                code += (" %" + lineNumber + " = mul i32 " + num1 + "," + num2+ "\n");
            }else if(line1==0 && line2!=0){
                lineNumber++;
                code += (" %" + lineNumber + " = mul i32 " + num1 + ",%" + line2+ "\n");
            }else if(line1!=0 && line2==0){
                lineNumber++;
                code += (" %" + lineNumber + " = mul i32 %" + line1 + "," + num2+ "\n");
            }else{
                lineNumber++;
                code += (" %" + lineNumber + " = mul i32 %" + line1 + ",%" + line2+ "\n");
            }
            return num1 * num2;
        }else {
            if(line1==0 && line2==0) {
                lineNumber++;
                code += (" %" + lineNumber + " = sdiv i32 " + num1 + "," + num2+ "\n");
            }else if(line1==0 && line2!=0){
                lineNumber++;
                code += (" %" + lineNumber + " = sdiv i32 " + num1 + ",%" + line2+ "\n");
            }else if(line1!=0 && line2==0){
                lineNumber++;
                code += (" %" + lineNumber + " = sdiv i32 %" + line1 + "," + num2+ "\n");
            }else{
                lineNumber++;
                code += (" %" + lineNumber + " = sdiv i32 %" + line1 + ",%" + line2+ "\n");
            }
            return num1 / num2;
        }
    }

    //Writes printing command into the output file
    //If there is any expression instead of a variable does the calculation first
    public static void printVariable(String expr){
        expr = infixToPostfix(expr);
        int value = calculate(expr);
        if(expr.replaceAll(" ","").equals(Integer.toString(value))) {
            code += (" call i32 (i8*, ...)* @printf(i8* getelementptr ([4 x i8]* @print.str, i32 0, i32 0)," +
                    " i32 " + (value) + " )\n");
        }else{code += (" call i32 (i8*, ...)* @printf(i8* getelementptr ([4 x i8]* @print.str, i32 0, i32 0)," +
                " i32 %"+(lineNumber)+" )\n");}
        lineNumber++;
    }

}
