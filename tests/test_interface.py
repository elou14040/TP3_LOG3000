"""Tests statiques du gabarit ``templates/index.html``.

Le HTML est analysé sans navigateur : on vérifie que chaque bouton affiche le
caractère qu'il ajoute à l'écran, et que les boutons essentiels sont présents.
"""

from html.parser import HTMLParser
from pathlib import Path
import re

import pytest

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "index.html"


class ButtonCollector(HTMLParser):
    """Collecte les boutons du gabarit sous forme de paires (libellé, onclick).

    Attributes:
        buttons (list[tuple[str, str]]): Libellé visible (sans espaces autour)
            et valeur de l'attribut ``onclick`` de chaque ``<button>``.
    """

    def __init__(self):
        super().__init__()
        self.buttons = []
        self._current = None

    def handle_starttag(self, tag, attrs):
        """Commence un bouton en mémorisant son ``onclick``."""
        if tag == "button":
            self._current = {"onclick": dict(attrs).get("onclick", ""), "text": ""}

    def handle_data(self, data):
        """Accumule le texte affiché du bouton en cours."""
        if self._current is not None:
            self._current["text"] += data

    def handle_endtag(self, tag):
        """Termine le bouton en cours et l'ajoute à la liste."""
        if tag == "button" and self._current is not None:
            self.buttons.append((self._current["text"].strip(), self._current["onclick"]))
            self._current = None


def collect_buttons():
    """Analyse ``index.html`` et retourne ses boutons.

    Returns:
        list[tuple[str, str]]: Paires (libellé, onclick) dans l'ordre du document.
    """
    parser = ButtonCollector()
    parser.feed(TEMPLATE.read_text(encoding="utf-8"))
    return parser.buttons


def appended_value(onclick):
    """Extrait le caractère passé à ``appendToDisplay`` dans un ``onclick``.

    Args:
        onclick (str): Valeur de l'attribut, p. ex. ``"appendToDisplay('7')"``.

    Returns:
        str | None: Le caractère ajouté, ou ``None`` si le bouton n'appelle pas
        ``appendToDisplay`` (boutons ``C`` et ``=``).
    """
    match = re.search(r"appendToDisplay\('(.)'\)", onclick)
    return match.group(1) if match else None


# Paramétrage sur les boutons qui ajoutent un caractère : un cas de test par bouton,
# pour que le rapport pytest désigne précisément le bouton mal étiqueté.
APPEND_BUTTONS = [
    (label, appended_value(onclick))
    for label, onclick in collect_buttons()
    if appended_value(onclick) is not None
]


@pytest.mark.parametrize(
    "label, value", APPEND_BUTTONS, ids=[f"bouton-{value}" for _, value in APPEND_BUTTONS]
)
def test_button_label_matches_appended_value(label, value):
    """Le libellé visible d'un bouton est exactement le caractère qu'il ajoute à l'écran."""
    assert label == value


def test_all_digits_and_operators_present():
    """Les 10 chiffres et les 4 opérateurs ont chacun un bouton."""
    values = {value for _, value in APPEND_BUTTONS}
    assert values == set("0123456789+-*/")


def test_clear_and_equals_buttons_present():
    """Les boutons ``C`` (effacer) et ``=`` (calculer) sont présents."""
    labels = [label for label, _ in collect_buttons()]
    assert "C" in labels
    assert "=" in labels
