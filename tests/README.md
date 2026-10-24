# `tests/` – Tests automatisés

## Raison d'être

Ce répertoire contient la suite de tests automatisés de la calculatrice. Elle vérifie que
chaque composant respecte le comportement documenté (docstrings et README principal) et
sert de filet de sécurité : **tous les tests doivent passer avant de fusionner une pull
request dans `main`**.

## État actuel

**45 tests, tous verts** sur `main`. Lors de la première exécution, 12 tests échouaient et
ont révélé 5 bogues (issues #1 à #5), tous corrigés depuis — voir la section
[Historique des correctifs](../README.md#historique-des-correctifs) du README principal.

## Exécuter les tests

Depuis la **racine du dépôt**, avec l'environnement virtuel activé et les dépendances
installées (`pip install -r requirements.txt`, qui inclut pytest) :

| Commande | Effet |
|----------|-------|
| `python -m pytest` | Toute la suite |
| `python -m pytest -v` | Détail de chaque test |
| `python -m pytest tests/test_operators.py` | Un seul fichier |
| `python -m pytest tests/test_operators.py::test_subtract` | Un seul test |
| `python -m pytest -k divide` | Les tests dont le nom contient « divide » |

Le fichier `pytest.ini` à la racine configure pytest : il cherche les tests dans `tests/` et
ajoute la racine au chemin d'import, ce qui permet d'écrire `from app import calculate`.

## Fichiers et couverture

| Fichier              | Ce qui est testé |
|----------------------|------------------|
| `conftest.py`        | Fixture `client` partagée : client de test Flask, qui envoie des requêtes sans lancer de serveur. |
| `test_operators.py`  | **Unitaire** : `add`, `subtract`, `multiply`, `divide` de `operators.py`, appelées directement. Résultats usuels, décimaux, ordre des opérandes, produit par zéro, quotient réel, division par zéro. |
| `test_calculate.py`  | **Analyse d'expression** : `calculate` de `app.py`. Les 4 opérations de bout en bout, espaces ignorés, décimaux, type `float` du résultat, et le message `ValueError` de chaque expression invalide (vide, plusieurs opérateurs, sans opérateur, opérateur au début/à la fin, opérande non numérique). |
| `test_app.py`        | **Intégration** : route `/`. GET (page 200, écran vide, CSS chargé), POST valide (résultat affiché), POST invalide et division par zéro (message `Error: ...` au lieu d'une page 500), POST sans champ `display`. |
| `test_interface.py`  | **Gabarit HTML** : `templates/index.html` analysé sans navigateur. Chaque bouton affiche exactement le caractère qu'il ajoute à l'écran (un cas par bouton), les 10 chiffres et 4 opérateurs sont présents, ainsi que `C` et `=`. |

### Non couvert

- Le comportement JavaScript dans un vrai navigateur (clics, effacement) : il faudrait un
  outil comme Selenium ou Playwright.
- Le rendu visuel du CSS.
- Les cas hors portée du projet (nombres négatifs, expressions à plusieurs opérateurs),
  sauf pour vérifier qu'ils produisent bien une erreur.

## Dépendances et hypothèses

- **pytest** ≥ 8 (dans `requirements.txt`).
- Les tests se lancent depuis la racine du dépôt (là où se trouve `pytest.ini`).
- Les résultats attendus proviennent des docstrings de `operators.py` / `app.py` et des
  exemples du README principal : si le comportement voulu change, il faut mettre à jour la
  documentation **et** les tests.
- Les comparaisons de décimaux non exacts utilisent `pytest.approx` (p. ex. `0.1 + 0.2`).
