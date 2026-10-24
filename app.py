"""Serveur Flask de la calculatrice web.

Ce module expose une seule page (``/``) qui affiche la calculatrice et reçoit
l'expression saisie par l'utilisateur. L'expression est analysée par
``calculate``, qui délègue l'opération aux fonctions de ``operators.py``.

Lancement : ``python app.py`` (mode debug, port 5000 par défaut).
"""

from flask import Flask, request, render_template
from operators import add, subtract, multiply, divide

app = Flask(__name__)

# Table de correspondance symbole -> fonction : ajouter un opérateur se fait
# ici, sans modifier l'analyse de l'expression.
OPS = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}

def calculate(expr: str):
    """Évalue une expression arithmétique simple de la forme ``a<op>b``.

    L'expression doit contenir exactement deux opérandes et un seul
    opérateur parmi ``+``, ``-``, ``*`` et ``/``. Les espaces sont ignorés.

    Args:
        expr (str): Expression à évaluer, p. ex. ``"12 + 3.5"``.

    Returns:
        float: Le résultat de l'opération appliquée aux deux opérandes.

    Raises:
        ValueError: Si l'expression est vide, contient plus d'un opérateur,
            n'a pas d'opérande d'un côté de l'opérateur, ou si un opérande
            n'est pas un nombre.
        ZeroDivisionError: Si l'opération est une division par zéro.
    """
    if not expr or not isinstance(expr, str):
        raise ValueError("empty expression")

    s = expr.replace(" ", "")

    op_pos = -1
    op_char = None

    # Chaque caractère qui est un opérateur est considéré comme LE séparateur ;
    # en trouver un second rend l'expression invalide (une seule opération permise).
    for i, ch in enumerate(s):
        if ch in OPS:
            if op_pos != -1:
                raise ValueError("only one operator is allowed")
            op_pos = i
            op_char = ch

    if op_pos <= 0 or op_pos >= len(s) - 1:
        # operator at start/end or not found
        raise ValueError("invalid expression format")

    left = s[:op_pos]
    right = s[op_pos+1:]

    try:
        a = float(left)
        b = float(right)
    except ValueError:
        # Message uniforme pour l'utilisateur plutôt que l'erreur brute de float().
        raise ValueError("operands must be numbers")

    return OPS[op_char](a, b)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Affiche la calculatrice et traite l'expression soumise.

    - ``GET`` : affiche la calculatrice avec un écran vide.
    - ``POST`` : lit le champ ``display`` du formulaire, l'évalue avec
      ``calculate`` et réaffiche la page avec le résultat.

    Returns:
        str: La page HTML ``index.html`` rendue, dont l'écran contient le
        résultat du calcul ou un message ``"Error: ..."``.
    """
    result = ""
    if request.method == 'POST':
        expression = request.form.get('display', '')
        try:
            result = calculate(expression)
        except Exception as e:
            # Toute erreur (format, division par zéro, etc.) est affichée à l'écran
            # au lieu de renvoyer une page d'erreur 500 à l'utilisateur.
            result = f"Error: {e}"
    return render_template('index.html', result=result)

if __name__ == '__main__':
    # debug=True : rechargement automatique et traces détaillées, pour le développement seulement.
    app.run(debug=True)
