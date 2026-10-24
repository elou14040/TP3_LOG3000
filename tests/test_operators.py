"""Tests unitaires des opérations arithmétiques de ``operators.py``.

Chaque fonction est testée isolément, sans passer par l'analyse de l'expression,
pour qu'un échec désigne directement l'opération fautive.
"""

import pytest

from operators import add, subtract, multiply, divide


def test_add():
    """``add`` retourne la somme des deux opérandes."""
    assert add(7, 5) == 12


def test_add_decimals():
    """``add`` gère les décimaux (comparaison approchée à cause des flottants)."""
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_subtract():
    """``subtract`` retourne ``a - b`` : l'ordre des opérandes compte."""
    assert subtract(9, 4) == 5


def test_subtract_negative_result():
    """``subtract`` retourne un résultat négatif quand ``b > a``."""
    assert subtract(4, 9) == -5


def test_multiply():
    """``multiply`` retourne le produit ``a * b``."""
    assert multiply(6, 4) == 24


def test_multiply_by_zero():
    """Un produit par zéro vaut zéro (``6 ** 0`` vaudrait 1, d'où l'intérêt du cas)."""
    assert multiply(6, 0) == 0


def test_divide():
    """``divide`` retourne le quotient réel, pas la division entière."""
    assert divide(6, 4) == 1.5


def test_divide_exact():
    """``divide`` d'un multiple exact."""
    assert divide(8, 2) == 4


def test_divide_by_zero_raises():
    """Diviser par zéro lève ``ZeroDivisionError`` (affichée ensuite comme erreur par l'app)."""
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
