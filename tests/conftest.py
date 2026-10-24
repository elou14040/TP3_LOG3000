"""Fixtures pytest partagées par tous les fichiers de tests."""

import pytest

from app import app as flask_app


@pytest.fixture
def client():
    """Fournit un client de test Flask pour envoyer des requêtes sans lancer de serveur.

    Aucun paramètre.

    Yields:
        flask.testing.FlaskClient: Client lié à l'application en mode test
        (les exceptions remontent au lieu de produire une page 500).
    """
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client
