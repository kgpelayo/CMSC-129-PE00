import tkinter as tk
from tkinter import filedialog, messagebox

# Math Functions

# Defines the precedence and order of operations
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/' or op == '%':
        return 2
    return 0

# Applies the operation to the operands
def apply_op(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError  # Flag zero division errors
        return a / b
    if op == '%':
        if b == 0:
            raise ZeroDivisionError
        return a % b

# Evaluates the postfix expression
def evaluate_postfix(exp, variables):
    stack = []
    for token in exp:
        if token.isdigit():  # Given that /token/ is a number
            stack.append(int(token))
        elif token in variables:  # Given that /token/ is a variable
            stack.append(variables[token])
        else:  # Given that /token/ is an operator
            b = stack.pop()
            a = stack.pop()
            stack.append(apply_op(a, b, token))
    return stack.pop()

# Reformats the infix expression into postfix for ease of computing
def infix_to_postfix(expression):
    output = []
    ops_stack = []
    tokens = expression.split()

    for token in tokens:
        if token.isalnum():  # Given /token/ is a variable or number
            output.append(token)
        elif token == '(':
            ops_stack.append(token)
        elif token == ')':
            while ops_stack and ops_stack[-1] != '(':
                output.append(ops_stack.pop())
            ops_stack.pop()
        else:  # Given /token/ is an operator
            while (ops_stack and precedence(ops_stack[-1]) >= precedence(token)):
                output.append(ops_stack.pop())
            ops_stack.append(token)

    while ops_stack:
        output.append(ops_stack.pop())

    return output

# Function to handle the input
def process_code(code, variables, errors, used_vars):
    try:
        if '=' in code:  # Assignment statement
            var, expr = code.split('=')
            var = var.strip()
            if not var.isalpha() or len(var) == 0:
                raise SyntaxError("Invalid variable name.")

            postfix_expr = infix_to_postfix(expr.strip())
            value = evaluate_postfix(postfix_expr, variables)
            variables[var] = value
            used_vars.add(var)
            return var, postfix_expr, value
        else:  # Just an expression
            postfix_expr = infix_to_postfix(code.strip())
            value = evaluate_postfix(postfix_expr, variables)
            return None, postfix_expr, value
    except ZeroDivisionError:
        errors.append("Division by zero")
        return None, [], "Error: Division by zero"
    except KeyError as e:
        errors.append(f"Undefined variable {e}")
        return None, [], f"Error: Undefined variable {e}"
    except Exception as e:
        errors.append(str(e))
        return None, [], f"Error: {str(e)}"

def on_process():
    input_text = input_area.get("1.0", "end-1c")
    output_area.delete("1.0", tk.END)

    variables = {}
    errors = []
    used_vars = set()

    lines = input_text.splitlines()

    output_area.insert(tk.END, "Input lines:\n" + input_text + "\n\nOutput:\n")

    for i, line in enumerate(lines, start=1):
        line = line.strip()
        if line:
            var, postfix_expr, result = process_code(line, variables, errors, used_vars)
            output_area.insert(tk.END, f"Line {i}: {line}\n")
            output_area.insert(tk.END, f"Postfix: {' '.join(postfix_expr)}\n")
            output_area.insert(tk.END, f"Result: {result}\n\n")

    output_area.insert(tk.END, "-------------------------------------------\n")
    output_area.insert(tk.END, "Variables used:\n")
    if used_vars:
        for var in used_vars:
            output_area.insert(tk.END, f"{var}\n")
    else:
        output_area.insert(tk.END, "No variables were used\n")
    
    output_area.insert(tk.END, "-------------------------------------------\n")
    output_area.insert(tk.END, "Errors found:\n")
    if errors:
        for error in errors:
            output_area.insert(tk.END, f"{error}\n")
    else:
        output_area.insert(tk.END, "No errors detected\n")

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                content = file.read()
                input_area.delete("1.0", tk.END)
                input_area.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Code Processor")

# Input area
input_label = tk.Label(root, text="Input Code:")
input_label.pack()
input_area = tk.Text(root, height=10, width=50)
input_area.pack()

# Upload button
upload_button = tk.Button(root, text="Upload .txt File", command=upload_file)
upload_button.pack()

# Process button
process_button = tk.Button(root, text="Process", command=on_process)
process_button.pack()

# Output area
output_label = tk.Label(root, text="Output:")
output_label.pack()
output_area = tk.Text(root, height=15, width=50)
output_area.pack()

# Run the GUI loop
root.mainloop()
