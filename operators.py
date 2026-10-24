"""Opérations arithmétiques de base utilisées par la calculatrice.

Chaque fonction reçoit deux opérandes numériques (déjà convertis en ``float``
par ``app.calculate``) et retourne le résultat de l'opération correspondante.
Ce module ne fait aucune validation des entrées : il suppose que l'appelant
lui transmet des nombres.
"""


def add(a,b):
    """Additionne deux nombres.

    Args:
        a (float): Opérande de gauche.
        b (float): Opérande de droite.

    Returns:
        float: La somme ``a + b``.
    """
    return a + b

def subtract(a,b):
    """Soustrait le second nombre du premier.

    Args:
        a (float): Opérande de gauche (diminuende).
        b (float): Opérande de droite (diminuteur).

    Returns:
        float: La différence ``a - b``.
    """
    return b - a

def multiply(a,b):
    """Multiplie deux nombres.

    Args:
        a (float): Opérande de gauche.
        b (float): Opérande de droite.

    Returns:
        float: Le produit ``a * b``.
    """
    return a ** b

def divide(a,b):
    """Divise le premier nombre par le second.

    Args:
        a (float): Dividende.
        b (float): Diviseur.

    Returns:
        float: Le quotient réel ``a / b``.

    Raises:
        ZeroDivisionError: Si ``b`` vaut 0.
    """
    return a / b
