from rpn import infix_to_polish, calculate_polish

if __name__ == "__main__":
    print("Это польский калькулятор")
    print("Для выхода введите 'q'")

    while True:
        expr = input("Введите выражение: ").strip()
        if expr.lower() == "q":
            print("Выход из программы.")
            break
        try:
            polish = infix_to_polish(expr)
            result = calculate_polish(polish)
            print(f"Результат: {result}")
        except ValueError as e:
            print("Ошибка:", e)
