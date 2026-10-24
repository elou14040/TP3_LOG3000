"""Tests de la route Flask ``/`` (intégration serveur + gabarit).

Les requêtes passent par le client de test (fixture ``client`` de ``conftest.py``),
comme le ferait le formulaire de la page.
"""

import re


def display_value(response):
    """Extrait la valeur affichée dans l'écran de la calculatrice.

    Args:
        response: Réponse Flask contenant la page ``index.html`` rendue.

    Returns:
        str: Contenu de l'attribut ``value`` du champ ``#display``.
    """
    html = response.get_data(as_text=True)
    match = re.search(r'id="display" value="([^"]*)"', html)
    assert match, "le champ #display est introuvable dans la page"
    return match.group(1)


def test_get_index_shows_empty_calculator(client):
    """Un GET affiche la page (200) avec un écran vide."""
    response = client.get("/")
    assert response.status_code == 200
    assert display_value(response) == ""


def test_get_index_loads_stylesheet(client):
    """La page référence bien la feuille de style servie par ``static/``."""
    html = client.get("/").get_data(as_text=True)
    assert "/static/style.css" in html


def test_post_displays_result(client):
    """Un POST d'une expression valide affiche le résultat dans l'écran."""
    response = client.post("/", data={"display": "7+5"})
    assert response.status_code == 200
    assert display_value(response) == "12.0"


def test_post_invalid_expression_displays_error(client):
    """Une expression invalide affiche ``Error: ...`` au lieu d'une page d'erreur."""
    response = client.post("/", data={"display": "5+"})
    assert response.status_code == 200
    assert display_value(response) == "Error: invalid expression format"


def test_post_division_by_zero_displays_error(client):
    """La division par zéro est attrapée par la route et affichée comme erreur."""
    response = client.post("/", data={"display": "5/0"})
    assert response.status_code == 200
    assert display_value(response).startswith("Error:")


def test_post_without_display_field(client):
    """Un POST sans champ ``display`` est traité comme une expression vide."""
    response = client.post("/", data={})
    assert display_value(response) == "Error: empty expression"
