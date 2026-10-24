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

    Sans argument à la construction; feed(html) remplit la liste buttons.
    """

    def __init__(self):
        """Initialise les collections de boutons.

        Aucun paramètre. Ne retourne aucune valeur; initialise buttons et _current.
        """
        super().__init__()
        self.buttons = []
        self._current = None

    def handle_starttag(self, tag, attrs):
        """Mémorise les attributs du bouton rencontré.

        Args:
            tag (str): Nom de la balise ouvrante.
            attrs (list[tuple[str, str | None]]): Attributs fournis par HTMLParser.

        Returns:
            None: Met à jour le bouton en cours si tag vaut "button".
        """
        if tag == "button":
            self._current = {"onclick": dict(attrs).get("onclick", ""), "text": ""}

    def handle_data(self, data):
        """Accumule le texte du bouton en cours.

        Args:
            data (str): Fragment de texte fourni par HTMLParser.

        Returns:
            None: Ajoute data au texte du bouton en cours, s’il existe.
        """
        if self._current is not None:
            self._current["text"] += data

    def handle_endtag(self, tag):
        """Enregistre le bouton à la fermeture de sa balise.

        Args:
            tag (str): Nom de la balise fermante.

        Returns:
            None: Complète buttons et termine le bouton en cours.
        """
        if tag == "button" and self._current is not None:
            self.buttons.append((self._current["text"].strip(), self._current["onclick"]))
            self._current = None


def collect_buttons():
    """Analyse ``index.html`` et retourne ses boutons.

    Aucun paramètre; lit le fichier désigné par TEMPLATE.

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
    """Le libellé visible d'un bouton est exactement le caractère qu'il ajoute à l'écran.

    Args:
        label: str: Texte visible du bouton.
        value: str: Caractère ajouté à l’écran par ce bouton.

    Returns:
        None: Vérifie le résultat par assertions.
    """
    assert label == value


def test_all_digits_and_operators_present():
    """Les 10 chiffres et les 4 opérateurs ont chacun un bouton.

    Aucun paramètre ni valeur de retour; vérification par assertions.
    """
    values = {value for _, value in APPEND_BUTTONS}
    assert values == set("0123456789+-*/")


def test_clear_and_equals_buttons_present():
    """Les boutons ``C`` (effacer) et ``=`` (calculer) sont présents.

    Aucun paramètre ni valeur de retour; vérification par assertions.
    """
    labels = [label for label, _ in collect_buttons()]
    assert "C" in labels
    assert "=" in labels
