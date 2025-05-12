import tkinter as tk
import math
import re

class ModernCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧠 Pro Scientific Calculator")
        self.geometry("750x640")
        self.configure(bg="#121212")
        self.resizable(False, False)

        self.expression = ""
        self.history = []

        self.create_gradient_background()
        self.create_display()
        self.create_main_layout()

    def create_gradient_background(self):
        self.bg_canvas = tk.Canvas(self, width=750, height=640, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)
        for i in range(0, 640):
            r = int(18 + (30 - 18) * (i / 640))
            g = int(18 + (30 - 18) * (i / 640))
            b = int(18 + (40 - 18) * (i / 640))
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.bg_canvas.create_line(0, i, 750, i, fill=color)

    def create_display(self):
        self.display = tk.Entry(self, font=("Segoe UI", 26), bg="#1e1e1e", fg="#00FFAA",
                                bd=0, relief="flat", justify="right", insertbackground="white")
        self.display.place(x=15, y=20, width=480, height=60)

    def create_main_layout(self):
        self.btn_frame = tk.Frame(self, bg="#121212")
        self.btn_frame.place(x=15, y=100, width=480, height=520)

        self.create_buttons()

        self.history_frame = tk.Frame(self, bg="#1e1e1e")
        self.history_frame.place(x=510, y=20, width=225, height=600)

        history_title = tk.Label(self.history_frame, text="History", bg="#1e1e1e",
                                 fg="white", font=("Segoe UI", 16, "bold"))
        history_title.pack(pady=(10, 5))

        self.history_list = tk.Listbox(self.history_frame, bg="#2c2c2c", fg="#00FFAA",
                                       font=("Consolas", 12), bd=0, highlightthickness=0)
        self.history_list.pack(fill="both", expand=True, padx=10, pady=10)

        ask_ai_btn = tk.Button(self.history_frame, text="Ask AI 🤖", font=("Segoe UI", 12, "bold"),
                               bg="#00FFAA", fg="black", relief="flat", command=self.ask_ai_popup)
        ask_ai_btn.pack(pady=10)

    def ask_ai_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Ask AI")
        popup.geometry("250x120")
        popup.configure(bg="#1e1e1e")
        label = tk.Label(popup, text="Coming soon...", font=("Segoe UI", 14),
                         bg="#1e1e1e", fg="white")
        label.pack(pady=30)

    def create_buttons(self):
        buttons = [
            "7", "8", "9", "/", "sin", "cos",
            "4", "5", "6", "*", "tan", "sqrt",
            "1", "2", "3", "-", "log", "ln",
            "0", ".", "=", "+", "(", ")",
            "^", "pi", "e", "mod", "!", "C"
        ]

        for i, label in enumerate(buttons):
            row, col = divmod(i, 6)
            btn = tk.Label(self.btn_frame, text=label, width=6, height=2,
                           font=("Segoe UI", 14, "bold"), fg="white", bg="#2c2c2c",
                           bd=0, relief="flat", padx=4, pady=4, justify="center")
            btn.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            btn.bind("<Button-1>", lambda e, l=label: self.button_click(l))
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#444444"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2c2c2c"))

        for i in range(6):
            self.btn_frame.columnconfigure(i, weight=1)
        for i in range(6):
            self.btn_frame.rowconfigure(i, weight=1)

    def button_click(self, label):
        if label == "C":
            self.expression = ""
        elif label == "=":
            self.evaluate_expression()
        else:
            self.expression += str(label)
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def evaluate_expression(self):
        try:
            expr = self.expression
            expr = expr.replace("pi", str(math.pi)).replace("e", str(math.e))
            expr = expr.replace("^", "**").replace("mod", "%")
            expr = expr.replace("sqrt", "sqrt_").replace("log", "log10_")
            expr = expr.replace("ln", "log_")

            functions = {
                "sqrt_": math.sqrt,
                "log10_": math.log10,
                "log_": math.log,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
            }

            expr = self.handle_factorials(expr)
            result = eval(expr, {"__builtins__": None}, functions)
            self.history.append(f"{self.expression} = {result}")
            self.history_list.insert(tk.END, f"{self.expression} = {result}")
            self.expression = str(result)
        except Exception:
            self.expression = "Error"

    def handle_factorials(self, expr):
        pattern = r'(\d+|\([^()]*\))!'
        while "!" in expr:
            match = re.search(pattern, expr)
            if not match:
                break
            val = match.group(1)
            if val.startswith("("):
                inner_expr = val[1:-1]
                computed = eval(inner_expr, {"__builtins__": None}, {
                    "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "log": math.log10, "sqrt": math.sqrt
                })
                fact = math.factorial(int(computed))
            else:
                fact = math.factorial(int(val))
            expr = expr.replace(f"{val}!", str(fact), 1)
        return expr

if __name__ == "__main__":
    ModernCalculator().mainloop()

