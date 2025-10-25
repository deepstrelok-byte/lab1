def infix_to_polish(expression):
    output = [] #выражение
    stack = [] #стек операторов
    priority = {'+': 1, '-': 1, '*': 2, '/': 2, '**': 3}

    i = 0
    while i < len(expression):
        char = expression[i]
        if char == ' ': #пропуск пробелов
            i += 1
            continue

        # Обработка чисел
        if char.isdigit() or char == '.':
            num_str = char
            i += 1
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num_str += expression[i]
                i += 1
            output.append(num_str)
            continue

        elif char == '*' and i + 1 < len(expression) and expression[i + 1] == '*':
            while (stack and stack[-1] != '(' and
                   priority.get(stack[-1], 0) >= priority.get('**', 0)):
                output.append(stack.pop())
            stack.append('**')
            i += 2
            continue

        # Обработка отрицательных чисел (унарный минус)
        elif char == '-' and (i == 0 or expression[i - 1] in '(+*-/**') : #если минус в начале или после операторов
            if i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                num_str = '-'
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                output.append(num_str)
                continue
            else:
                # Это бинарная операция
                while (stack and stack[-1] != '(' and
                       priority.get(stack[-1], 0) >= priority.get(char, 0)):  #пока стек не пуст и сверху не скобка продолжаем сравнивать приоритеты
                    output.append(stack.pop()) #если оператор с большим/равным приоритетом, выталкиваем в аутпут
                stack.append(char)
                i += 1
                continue

        # Теперь обработка бинарных операторов
        elif char in '+-*/' or (char == '*' and i + 1 < len(expression) and expression[i + 1] == '*'):
            while (stack and stack[-1] != '(' and
                   priority.get(stack[-1], 0) >= priority.get(char, 0)):
                output.append(stack.pop())
            stack.append(char)

        elif char == '(':
            stack.append(char)

        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()  # удаляем (

        i += 1

    # толкаем оставшиеся операторы из стека
    while stack:
        output.append(stack.pop())

    return ' '.join(output)


# Вычисляем в польской нотации
def calculate_polish(expression):
    stack = []
    tokens = expression.split()

    for token in tokens:
        if token in ['+', '-', '*', '**', '/']:
            if len(stack) < 2:
                raise ValueError(f"Мало чисел для операции '{token}'")

            b = stack.pop()
            a = stack.pop()

            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '**':
                result = a ** b
            elif token == '/':
                if b == 0:
                    raise ValueError("Деление на ноль")
                result = a / b

            stack.append(result)
        else:
            try:
                number = float(token)
                stack.append(number)
            except ValueError:
                raise ValueError(f"Неизвестный токен: {token}")

    if len(stack) != 1:
        raise ValueError(f"Некорректное выражение. В стеке остались необработанные числа: {stack}")

    return stack[0]

if __name__ == "__main__":
        user_input = input("Введите выражение: ").strip()
        try:
            polish = infix_to_polish(user_input)
            result = calculate_polish(polish)
            print("Результат:", result)
        except ValueError as e:
            print("Ошибка:", e)
