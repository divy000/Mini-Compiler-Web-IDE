import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import scrolledtext
from parser import parser
from semantic import semantic_analysis
from intermediate import generate_tac
from interpreter import execute_tac
import io
import sys
import re

# ------------------ RUN COMPILER ------------------
def run_compiler():
    code = input_text.get("1.0", tk.END)

    output_text.config(state="normal")
    tac_text.config(state="normal")

    output_text.delete("1.0", tk.END)
    tac_text.delete("1.0", tk.END)

    try:
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()

        ast = parser.parse(code)

        print("===== AST =====")
        print(ast)

        print("\n===== SEMANTIC OUTPUT =====")
        semantic_analysis(ast)

        print("\n===== FINAL OUTPUT =====")
        execute_tac(generate_tac(ast))

        tac = generate_tac(ast)

        # Show TAC in separate tab
        for line in tac:
            tac_text.insert(tk.END, line + "\n")

        sys.stdout = old_stdout
        output_text.insert(tk.END, mystdout.getvalue())

    except Exception as e:
        sys.stdout = old_stdout
        highlight_error(str(e))
        output_text.insert(tk.END, f"ERROR:\n{e}")

    output_text.config(state="disabled")
    tac_text.config(state="disabled")


# ------------------ CLEAR ------------------
def clear_all():
    input_text.delete("1.0", tk.END)
    output_text.config(state="normal")
    tac_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    tac_text.delete("1.0", tk.END)
    output_text.config(state="disabled")
    tac_text.config(state="disabled")


# ------------------ FILE OPS ------------------
def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        with open(file, "w") as f:
            f.write(input_text.get("1.0", tk.END))


def load_file():
    file = filedialog.askopenfilename()
    if file:
        with open(file, "r") as f:
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, f.read())


# ------------------ SYNTAX HIGHLIGHT ------------------
def highlight_syntax(event=None):
    content = input_text.get("1.0", tk.END)

    input_text.tag_remove("keyword", "1.0", tk.END)
    input_text.tag_remove("number", "1.0", tk.END)
    input_text.tag_remove("operator", "1.0", tk.END)

    for word in ["int", "if", "print"]:
        for match in re.finditer(rf"\b{word}\b", content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            input_text.tag_add("keyword", start, end)

    for match in re.finditer(r"\b\d+\b", content):
        start = f"1.0 + {match.start()} chars"
        end = f"1.0 + {match.end()} chars"
        input_text.tag_add("number", start, end)

    for match in re.finditer(r"[+\-*/=<>]", content):
        start = f"1.0 + {match.start()} chars"
        end = f"1.0 + {match.end()} chars"
        input_text.tag_add("operator", start, end)


# ------------------ ERROR HIGHLIGHT ------------------
def highlight_error(message):
    input_text.tag_remove("error", "1.0", tk.END)
    # simple highlight first line
    input_text.tag_add("error", "1.0", "1.end")


# ------------------ LINE NUMBERS ------------------
def update_line_numbers(event=None):
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", tk.END)

    lines = input_text.get("1.0", tk.END).split("\n")
    for i in range(len(lines)):
        line_numbers.insert(tk.END, str(i+1) + "\n")

    line_numbers.config(state="disabled")


# ------------------ UI SETUP ------------------
root = tk.Tk()
root.title("Mini Compiler IDE")
root.geometry("1000x650")
root.configure(bg="#1e1e1e")

# ------------------ TOP BAR ------------------
top_frame = tk.Frame(root, bg="#1e1e1e")
top_frame.pack(fill="x")

tk.Button(top_frame, text="▶ Run", command=run_compiler,
          bg="#007acc", fg="white").pack(side="left", padx=5, pady=5)

tk.Button(top_frame, text="🧹 Clear", command=clear_all,
          bg="#cc3300", fg="white").pack(side="left", padx=5)

tk.Button(top_frame, text="💾 Save", command=save_file,
          bg="#444", fg="white").pack(side="left", padx=5)

tk.Button(top_frame, text="📂 Load", command=load_file,
          bg="#444", fg="white").pack(side="left", padx=5)

# ------------------ NOTEBOOK (TABS) ------------------
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ------------------ EDITOR TAB ------------------
editor_frame = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(editor_frame, text="Editor")

line_numbers = tk.Text(editor_frame, width=4, bg="#2d2d2d", fg="white")
line_numbers.pack(side="left", fill="y")

input_text = scrolledtext.ScrolledText(editor_frame, font=("Consolas", 12),
                                       bg="#252526", fg="white",
                                       insertbackground="white")
input_text.pack(fill="both", expand=True)

input_text.bind("<KeyRelease>", highlight_syntax)
input_text.bind("<KeyRelease>", update_line_numbers)

input_text.tag_config("keyword", foreground="#569CD6")
input_text.tag_config("number", foreground="#B5CEA8")
input_text.tag_config("operator", foreground="#D4D4D4")
input_text.tag_config("error", background="#ff4d4d")

# ------------------ TAC TAB ------------------
tac_frame = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(tac_frame, text="TAC")

tac_text = scrolledtext.ScrolledText(tac_frame, font=("Consolas", 11),
                                     bg="#1e1e1e", fg="#00ffcc")
tac_text.pack(fill="both", expand=True)

# ------------------ OUTPUT TAB ------------------
output_frame = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(output_frame, text="Output")

output_text = scrolledtext.ScrolledText(output_frame, font=("Consolas", 11),
                                        bg="#1e1e1e", fg="#00ffcc")
output_text.pack(fill="both", expand=True)

output_text.config(state="disabled")
tac_text.config(state="disabled")

root.mainloop()