"""Калькулятор с кнопками (tkinter)."""

import ast
import operator
import tkinter as tk

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def evaluate(expression):
    """Безопасно считает выражение из чисел, + - * / и скобок.

    Возвращает строку с результатом. Бросает ValueError при ошибке.
    """
    expr = expression.replace("×", "*").replace("÷", "/").replace(",", ".").strip()
    if not expr:
        raise ValueError("пустое выражение")
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError:
        raise ValueError("ошибка в выражении")

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            left, right = walk(node.left), walk(node.right)
            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("деление на ноль")
            return _OPS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            value = walk(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        raise ValueError("ошибка в выражении")

    return format_number(walk(tree))


def format_number(value):
    if isinstance(value, float):
        if value.is_integer() and abs(value) < 1e15:
            return str(int(value))
        return f"{value:.10g}"
    return str(value)


class CalculatorApp:
    BUTTONS = [
        ["C", "⌫", "(", ")"],
        ["7", "8", "9", "÷"],
        ["4", "5", "6", "×"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
    ]

    def __init__(self, root):
        self.root = root
        root.title("Калькулятор")
        root.configure(bg="#202020")
        root.minsize(300, 420)

        self.display = tk.StringVar(value="0")
        self.just_calculated = False

        label = tk.Label(
            root, textvariable=self.display, anchor="e", padx=12,
            font=("Segoe UI", 28), bg="#202020", fg="white",
        )
        label.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(10, 5))

        for r, row in enumerate(self.BUTTONS, start=1):
            for c, text in enumerate(row):
                if text == "=":
                    bg, active = "#4c9be8", "#3a86d1"
                elif text in "÷×-+":
                    bg, active = "#3b3b3b", "#4a4a4a"
                elif text in ("C", "⌫", "(", ")"):
                    bg, active = "#323232", "#424242"
                else:
                    bg, active = "#2d2d2d", "#3d3d3d"
                btn = tk.Button(
                    root, text=text, font=("Segoe UI", 18), bd=0,
                    bg=bg, fg="white", activebackground=active, activeforeground="white",
                    command=lambda t=text: self.press(t),
                )
                btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        for c in range(4):
            root.columnconfigure(c, weight=1)
        for r in range(1, 6):
            root.rowconfigure(r, weight=1)

        root.bind("<Key>", self.on_key)

    def press(self, key):
        current = self.display.get()
        if key == "C":
            self.display.set("0")
        elif key == "⌫":
            self.display.set(current[:-1] or "0")
        elif key == "=":
            try:
                self.display.set(evaluate(current))
            except (ValueError, OverflowError) as e:
                self.display.set(f"Ошибка: {e}" if str(e) != "деление на ноль" else "На ноль делить нельзя")
            self.just_calculated = True
            return
        else:
            starts_over = current == "0" or current.startswith(("Ошибка", "На ноль"))
            if self.just_calculated and key not in "÷×-+":
                starts_over = True
            if starts_over and key not in "÷×-+":
                self.display.set(key)
            elif current.startswith(("Ошибка", "На ноль")):
                self.display.set("0" + key)
            else:
                self.display.set(current + key)
        self.just_calculated = False

    def on_key(self, event):
        mapping = {"*": "×", "/": "÷", "Return": "=", "KP_Enter": "=", "equal": "=",
                   "BackSpace": "⌫", "Escape": "C", "comma": "."}
        key = mapping.get(event.keysym) or mapping.get(event.char) or event.char
        if key and (key in "0123456789.+-()" or key in ("×", "÷", "=", "⌫", "C")):
            self.press(key)


def main():
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
