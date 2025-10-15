import pytest

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import RPNcalc_fin as rpn

@pytest.mark.parametrize("expr, expected", [
    ("1 + 2", "1 2 +"),
    ("3-1", "3 1 -"),
    ("2 * 3 + 4", "2 3 * 4 +"),  # приоритет *
    ("2 * (3 + 4)", "2 3 4 + *"),
    ("(1+2)*(3+4)", "1 2 + 3 4 + *"),
    ("-5 + 3", "-5 3 +"),           # унарный минус
    ("3.5 * 2", "3.5 2 *"),         # десятичные числа
    ("(2+3)*(-4+5)", "2 3 + -4 5 + *"),
])
def test_infix_to_polish_basic(expr, expected):
    assert rpn.infix_to_polish(expr) == expected


@pytest.mark.parametrize("rpn_expr, expected", [
    ("1 2 +", 3.0),
    ("3 1 -", 2.0),
    ("2 3 * 4 +", 10.0),
    ("2 3 4 + *", 14.0),
    ("3.5 2 *", 7.0),
    ("-5 3 +", -2.0),
])
def test_calculate_polish_basic(rpn_expr, expected):
    assert rpn.calculate_polish(rpn_expr) == expected

#Ошибочные случаи
def test_division_by_zero():
    with pytest.raises(ValueError, match="Деление на ноль"):
        rpn.calculate_polish("4 0 /")

def test_unknown_token():
    with pytest.raises(ValueError, match="Неизвестный токен"):
        rpn.calculate_polish("2 3 &")

def test_insufficient_operands():
    with pytest.raises(ValueError):
        rpn.calculate_polish("2 +")

def test_leftover_numbers():
    with pytest.raises(ValueError):
        rpn.calculate_polish("1 2 3 +")

@pytest.mark.parametrize("infix, expected", [
    ("1 + 2", 3.0),
    ("2 * (3 + 4)", 14.0),
    ("-5 + (4 * 2)", 3.0),
    ("(1.5 + 2.5) * 2", 8.0),
])
def test_infix_to_result(infix, expected):
    polish = rpn.infix_to_polish(infix)
    result = rpn.calculate_polish(polish)
    assert result == expected
