import tkinter as tk
from tkinter import messagebox

# Helper function: precedence of operators
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/' or op == '%':
        return 2
    return 0

# Helper function: apply an operator to two operands
def apply_op(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError
        return a / b
    if op == '%':
        if b == 0:
            raise ZeroDivisionError
        return a % b

# Function to evaluate a postfix expression
def evaluate_postfix(exp, variables):
    stack = []
    for token in exp:
        if token.isdigit():  # token is a number
            stack.append(int(token))
        elif token in variables:  # token is a variable
            stack.append(variables[token])
        else:  # token is an operator
            b = stack.pop()
            a = stack.pop()
            stack.append(apply_op(a, b, token))
    return stack.pop()

# Function to convert infix to postfix using the Shunting Yard algorithm
def infix_to_postfix(expression):
    output = []
    ops_stack = []
    tokens = expression.split()
    
    for token in tokens:
        if token.isalnum():  # token is a variable or a number
            output.append(token)
        elif token == '(':
            ops_stack.append(token)
        elif token == ')':
            while ops_stack and ops_stack[-1] != '(':
                output.append(ops_stack.pop())
            ops_stack.pop()
        else:  # token is an operator
            while (ops_stack and precedence(ops_stack[-1]) >= precedence(token)):
                output.append(ops_stack.pop())
            ops_stack.append(token)
    
    while ops_stack:
        output.append(ops_stack.pop())
    
    return output

# Function to process the code
def process_code(code, variables):
    try:
        if '=' in code:  # Assignment statement
            var, expr = code.split('=')
            var = var.strip()
            if not var.isalpha() or len(var) == 0:
                raise SyntaxError("Invalid variable name.")
            
            postfix_expr = infix_to_postfix(expr.strip())
            value = evaluate_postfix(postfix_expr, variables)
            variables[var] = value
            return f"{var} = {value}"
        else:  # Just an expression
            postfix_expr = infix_to_postfix(code.strip())
            value = evaluate_postfix(postfix_expr, variables)
            return str(value)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except KeyError as e:
        return f"Error: Undefined variable {e}"
    except Exception as e:
        return f"Error: {str(e)}"

# Function to handle the button click
def on_process():
    input_text = input_area.get("1.0", "end-1c")
    output_area.delete("1.0", tk.END)
    
    variables = {}
    lines = input_text.splitlines()
    
    for line in lines:
        result = process_code(line.strip(), variables)
        output_area.insert(tk.END, result + '\n')

# Create the main window
root = tk.Tk()
root.title("Code Processor")

# Input area
input_label = tk.Label(root, text="Input Code:")
input_label.pack()
input_area = tk.Text(root, height=10, width=50)
input_area.pack()

# Process button
process_button = tk.Button(root, text="Process", command=on_process)
process_button.pack()

# Output area
output_label = tk.Label(root, text="Output:")
output_label.pack()
output_area = tk.Text(root, height=10, width=50)
output_area.pack()

# Run the GUI loop
root.mainloop()
