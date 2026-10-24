"""Tests de la fonction ``calculate`` de ``app.py``.

On vérifie le résultat de bout en bout (analyse + opération) pour des expressions
valides, puis le message d'erreur pour chaque type d'expression invalide.
"""

import pytest

from app import calculate


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("7+5", 12.0),
        ("9-4", 5.0),
        ("6*4", 24.0),
        ("6/4", 1.5),
    ],
)
def test_calculate_basic_operations(expr, expected):
    """Chaque opérateur donne le résultat attendu (exemples du README)."""
    assert calculate(expr) == expected


def test_calculate_ignores_spaces():
    """Les espaces autour de l'opérateur et des opérandes sont ignorés."""
    assert calculate(" 12 + 3 ") == 15.0


def test_calculate_decimals():
    """Les opérandes décimaux sont acceptés."""
    assert calculate("2.5+0.5") == 3.0


def test_calculate_returns_float():
    """Le résultat est toujours un ``float``, même pour des opérandes entiers."""
    assert isinstance(calculate("2+2"), float)


@pytest.mark.parametrize(
    "expr, message",
    [
        ("", "empty expression"),
        ("1+2+3", "only one operator is allowed"),
        ("42", "invalid expression format"),
        ("5+", "invalid expression format"),
        ("+5", "invalid expression format"),
        ("1.2.3+4", "operands must be numbers"),
    ],
)
def test_calculate_invalid_expressions(expr, message):
    """Chaque expression invalide lève ``ValueError`` avec le message documenté dans le README."""
    with pytest.raises(ValueError, match=message):
        calculate(expr)


def test_calculate_division_by_zero():
    """La division par zéro remonte en ``ZeroDivisionError`` (gérée ensuite par la route)."""
    with pytest.raises(ZeroDivisionError):
        calculate("5/0")
