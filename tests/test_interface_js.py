"""Tests du comportement JavaScript de l'écran (``appendToDisplay`` / ``clearDisplay``).

La page est rendue par Flask (GET ou POST), puis son ``<script>`` est exécuté par Node.js
avec un faux ``document`` réduit au champ ``#display``. On simule ainsi des clics sur les
boutons sans lancer de navigateur. Les tests sont ignorés si Node.js n'est pas installé.
"""

import json
import re
import shutil
import subprocess

import pytest

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="Node.js n'est pas installé")

# Exécute le script de la page dans un contexte isolé, puis rejoue les clics reçus en entrée.
NODE_RUNNER = """
const vm = require('vm');
const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const display = { value: input.initial };
const context = { document: { getElementById: () => display } };
vm.createContext(context);
vm.runInContext(input.script, context);
for (const click of input.clicks) {
  vm.runInContext(click === 'C' ? 'clearDisplay()' : `appendToDisplay(${JSON.stringify(click)})`, context);
}
process.stdout.write(display.value);
"""


def click(response, clicks):
    """Simule une suite de clics sur la page rendue et retourne le contenu final de l'écran.

    Args:
        response: Réponse Flask contenant la page ``index.html`` rendue.
        clicks (list[str]): Caractères ajoutés par les boutons, ou ``"C"`` pour effacer.

    Returns:
        str: Valeur du champ ``#display`` après les clics.
    """
    html = response.get_data(as_text=True)
    script = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    initial = re.search(r'id="display" value="([^"]*)"', html).group(1)
    payload = json.dumps({"script": script, "initial": initial, "clicks": clicks})
    result = subprocess.run(["node", "-e", NODE_RUNNER], input=payload,
                            capture_output=True, text=True, check=True)
    return result.stdout


def test_digits_build_expression_on_empty_display(client):
    """Sur une page neuve, les chiffres et l'opérateur s'ajoutent à l'écran."""
    assert click(client.get("/"), ["1", "2", "+", "3"]) == "12+3"


def test_digit_after_result_starts_new_calculation(client):
    """Après un résultat, un chiffre remplace l'écran au lieu de s'ajouter au résultat."""
    response = client.post("/", data={"display": "7+5"})
    assert click(response, ["3"]) == "3"


def test_operator_after_result_continues_from_result(client):
    """Après un résultat, un opérateur s'ajoute au résultat pour enchaîner un calcul."""
    response = client.post("/", data={"display": "7+5"})
    assert click(response, ["+", "5"]) == "12.0+5"


def test_digit_after_error_starts_new_calculation(client):
    """Après un message d'erreur, un chiffre remplace le message."""
    response = client.post("/", data={"display": "5+"})
    assert click(response, ["4"]) == "4"


def test_second_digit_after_result_is_appended(client):
    """Une fois le nouveau calcul commencé, les chiffres suivants s'ajoutent normalement."""
    response = client.post("/", data={"display": "7+5"})
    assert click(response, ["3", "4"]) == "34"


def test_clear_then_digit(client):
    """Le bouton C vide l'écran, puis le chiffre suivant s'y ajoute."""
    response = client.post("/", data={"display": "7+5"})
    assert click(response, ["C", "9"]) == "9"
