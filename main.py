import tkinter as tk
from tkinter import filedialog, messagebox
import re

def precedence(op):
    """Determine the precedence of operators."""
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/' or op == '%':
        return 2
    return 0

def apply_op(a, b, op):
    """Apply the given operator to two operands."""
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

def evaluate_postfix(exp, variables):
    """Evaluate a postfix expression."""
    stack = []
    for token in exp:
        if token.isdigit():
            stack.append(int(token))
        elif token in variables:
            stack.append(variables[token])
        else:
            if len(stack) < 2:
                raise ValueError("Invalid input")  # Handles invalid input like "_"
            b = stack.pop()
            a = stack.pop()
            stack.append(apply_op(a, b, token))
    return stack.pop()

def tokenize(expression):
    """Convert an infix expression string into a list of tokens."""
    tokens = []
    i = 0
    length = len(expression)
    
    while i < length:
        if expression[i].isdigit():
            num = ''
            while i < length and expression[i].isdigit():
                num += expression[i]
                i += 1
            tokens.append(num)
        elif expression[i].isalpha():
            var = ''
            while i < length and expression[i].isalnum():
                var += expression[i]
                i += 1
            tokens.append(var)
        elif expression[i] in '+-*/()%':
            tokens.append(expression[i])
            i += 1
        else:
            i += 1  # Skip any unexpected characters

    return tokens

def infix_to_postfix(expression):
    """Convert an infix expression to a postfix expression."""
    output = []
    ops_stack = []
    tokens = tokenize(expression)

    for token in tokens:
        if token.isalnum():
            output.append(token)
        elif token == '(':
            ops_stack.append(token)
        elif token == ')':
            while ops_stack and ops_stack[-1] != '(':
                output.append(ops_stack.pop())
            ops_stack.pop()
        else:
            while (ops_stack and precedence(ops_stack[-1]) >= precedence(token)):
                output.append(ops_stack.pop())
            ops_stack.append(token)

    while ops_stack:
        output.append(ops_stack.pop())

    return output

def is_valid_variable_name(name):
    """Check if a given name is a valid C-style variable name."""
    return bool(re.match("^[a-zA-Z][a-zA-Z0-9]*$", name))

def process_code(line_num, code, variables, errors, used_vars):
    """Process a single line of code."""
    try:
        if '=' in code:
            var, expr = code.split('=')
            var = var.strip()
            expr = expr.strip()

            if not is_valid_variable_name(var):
                raise SyntaxError(f"Invalid variable name: {var}")

            tokens = tokenize(expr)
            for token in tokens:
                if token.isalnum() and not token.isdigit() and token not in variables:
                    errors.append(f"Line {line_num}: Undefined variable {token}")
                    return var, [], f"Error: Undefined variable {token}"

            postfix_expr = infix_to_postfix(expr)
            value = None
            try:
                value = evaluate_postfix(postfix_expr, variables)
                variables[var] = value  # Assign value after evaluation
                used_vars.add(var)
            except ZeroDivisionError:
                errors.append(f"Line {line_num}: Division by zero")
                return var, postfix_expr, "Error: Division by zero"
            return var, postfix_expr, value
        else:
            tokens = tokenize(code)
            if not tokens:
                raise ValueError("Invalid input")  # Empty or invalid expression like "_"

            for token in tokens:
                if token.isalnum() and not token.isdigit() and token not in variables:
                    errors.append(f"Line {line_num}: Undefined variable {token}")
                    return None, [], f"Error: Undefined variable {token}"

            postfix_expr = infix_to_postfix(code)
            value = evaluate_postfix(postfix_expr, variables)
            return None, postfix_expr, value
    except SyntaxError as e:
        errors.append(f"Line {line_num}: {str(e)}")
        return None, [], f"Error: {str(e)}"
    except ValueError as e:
        errors.append(f"Line {line_num}: {str(e)}")
        return None, [], f"Error: Invalid input"
    except Exception as e:
        errors.append(f"Line {line_num}: {str(e)}")
        return None, [], f"Error: {str(e)}"

def on_process():
    """Process the input code and display the results."""
    input_text = input_area.get("1.0", "end-1c")
    if not input_text.strip():
        messagebox.showerror("Error", "Input area is empty!")
        return

    output_area.config(state=tk.NORMAL)
    output_area.delete("1.0", tk.END)

    variables = {}
    errors = []
    used_vars = set()

    lines = input_text.splitlines()

    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if line:
            var, postfix_expr, result = process_code(i, line, variables, errors, used_vars)
            output_area.insert(tk.END, f"Line {i}: {line}\n")
            output_area.insert(tk.END, f"Postfix: {' '.join(postfix_expr)}\n")
            output_area.insert(tk.END, f"Result: {result}\n\n")

    output_area.insert(tk.END, "-------------------------------------------\n")
    output_area.insert(tk.END, "Variables used:\n")
    if used_vars:
        for var in used_vars:
            output_area.insert(tk.END, f"{var}: {variables[var]}\n")
    else:
        output_area.insert(tk.END, "No variables were used\n")

    output_area.insert(tk.END, "-------------------------------------------\n")
    output_area.insert(tk.END, "Errors found:\n")
    if errors:
        for error in errors:
            output_area.insert(tk.END, f"{error}\n")
    else:
        output_area.insert(tk.END, "No errors detected\n")
    output_area.config(state=tk.DISABLED)

def load_file():
    """Load the content of a file into the input area."""
    file_path = filedialog.askopenfilename(filetypes=[("Input files", "*.in")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            input_area.delete("1.0", tk.END)
            input_area.insert(tk.END, content)

root = tk.Tk()
root.title("PE 00: Expression Evaluation")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

input_label = tk.Label(root, text="Input Code:")
input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

input_area = tk.Text(root, height=20, width=50)
input_area.grid(row=1, column=0, padx=10, pady=10)

output_label = tk.Label(root, text="Output:")
output_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

output_area = tk.Text(root, height=20, width=50)
output_area.grid(row=1, column=1, padx=10, pady=10)
output_area.config(state=tk.DISABLED)

load_button = tk.Button(root, text="Load .in File", command=load_file)
load_button.grid(row=2, column=0, pady=10)

process_button = tk.Button(root, text="Process", command=on_process)
process_button.grid(row=2, column=1, pady=10)

root.mainloop()
