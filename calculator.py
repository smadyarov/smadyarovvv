def calculate(a, op, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("на ноль делить нельзя")
        return a / b
    raise ValueError(f"неизвестная операция: {op}")


def main():
    print("Калькулятор. Операции: + - * /")
    print("Для выхода введите q")
    while True:
        first = input("\nПервое число: ")
        if first.strip().lower() == "q":
            break
        op = input("Операция (+ - * /): ").strip()
        second = input("Второе число: ")
        try:
            result = calculate(float(first), op, float(second))
            print("Результат:", result)
        except ValueError as e:
            print("Ошибка:", e if "операция" in str(e) else "нужно ввести число")
        except ZeroDivisionError as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    main()
