# Calculatrice Web (Flask)

Application web simple de calculatrice, construite avec Python et la bibliothèque Flask.
Ce dépôt centralise le code, la documentation, les tests et le processus de collaboration
de l'équipe.

## Équipe

**Équipe n° 17** — LOG3000

| Membre           | Matricule |
|------------------|-----------|
| Ibrahima Gueye   | 2161023   |
| Mounder Chaourar | 2301906   |

## Table des matières

1. [But et portée du projet](#but-et-portée-du-projet)
2. [Structure du dépôt](#structure-du-dépôt)
3. [Prérequis](#prérequis)
4. [Installation](#installation)
5. [Utilisation](#utilisation)
6. [Tests](#tests)
7. [Flux de contribution](#flux-de-contribution)

## But et portée du projet

### But

Fournir une calculatrice web **simple, fiable et maintenable**. L'utilisateur compose une
expression à l'aide des boutons de l'interface. Le navigateur l'envoie au serveur Flask, qui
l'analyse, effectue le calcul et renvoie la page avec le résultat.

Au-delà de l'application, ce dépôt sert à mettre en place de bonnes pratiques de
développement en équipe : documentation du code, tests automatisés, suivi des bogues par
issues, une branche par correctif, pull requests et revues de code.

### Portée

**Inclus :**

- Les quatre opérations de base : addition (`+`), soustraction (`-`), multiplication (`*`) et
  division (`/`).
- Les nombres entiers et décimaux (p. ex. `2.5`).
- **Une seule opération par calcul**, de la forme `nombre opérateur nombre` (p. ex. `12+3`).
- Les messages d'erreur affichés à l'écran pour toute expression invalide.

**Hors portée (limites connues) :**

- Les expressions à plusieurs opérateurs (`1+2+3`) et les parenthèses.
- Les nombres négatifs saisis directement (`-5+3`, `5*-3`).
- Les fonctions avancées (puissance, racine, pourcentage, mémoire).
- La saisie au clavier : l'écran est en lecture seule et se remplit uniquement par les boutons.

### Architecture

```
Navigateur                          Serveur Flask
──────────                          ─────────────
index.html + style.css
  │ clics → JavaScript remplit l'écran
  │ bouton « = » → POST /  (champ "display")
  └──────────────────────────────►  app.py : index()
                                       └─ calculate(expr)   analyse "a<op>b"
                                            └─ operators.py add / subtract / multiply / divide
  ◄──────────────────────────────  index.html rendu avec le résultat (ou "Error: ...")
```

## Structure du dépôt

```
.
├── app.py              # Serveur Flask : route "/" et analyse de l'expression (calculate)
├── operators.py        # Opérations arithmétiques : add, subtract, multiply, divide
├── requirements.txt    # Dépendances Python
├── templates/          # Gabarits HTML (interface)       → voir templates/README.md
│   └── index.html
├── static/             # Fichiers statiques (style)      → voir static/README.md
│   └── style.css
└── tests/              # Tests automatisés (pytest)      → voir tests/README.md
```

### Modules backend (racine)

| Fichier        | Responsabilité |
|----------------|----------------|
| `app.py`       | Crée l'application Flask et définit la route `/` (`index`). La fonction `calculate(expr)` retire les espaces, repère l'unique opérateur, convertit les deux opérandes en `float` et appelle l'opération correspondante via la table `OPS`. Toute exception est convertie en message `Error: ...` affiché à l'écran. |
| `operators.py` | Quatre fonctions pures `add`, `subtract`, `multiply`, `divide`, qui prennent deux nombres et retournent le résultat. Aucune validation : elles supposent recevoir des nombres. |

Chaque sous-répertoire possède son propre `README.md` qui détaille son contenu, ses
dépendances et ses hypothèses.

## Prérequis

- Un compte GitHub (avec accès au dépôt)
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) 3.9 ou plus récent
- pip (inclus avec Python)

Pour vérifier les versions installées :

```bash
git --version
python3 --version
python3 -m pip --version
```

## Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/elou14040/TP3_LOG3000.git
   cd TP3_LOG3000
   ```

2. **Créer et activer un environnement virtuel** (recommandé, pour isoler les dépendances)

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

   Le nom `(venv)` doit apparaître au début de l'invite de commande.

3. **Installer les dépendances** (Flask et pytest)

   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Lancer l'application

Depuis la racine du dépôt, avec l'environnement virtuel activé :

```bash
python app.py
```

Ouvrez ensuite <http://127.0.0.1:5000> dans un navigateur. Pour arrêter le serveur,
faites `Ctrl + C` dans le terminal.

> **Note macOS :** le port 5000 est souvent occupé par le récepteur AirPlay (la page renvoie
> alors une erreur 403). Lancez plutôt l'application sur un autre port :
>
> ```bash
> flask --app app run --port 5001
> ```
>
> puis ouvrez <http://127.0.0.1:5001>.

### Faire un calcul

1. Cliquez sur les chiffres du premier nombre.
2. Cliquez sur un opérateur : `+`, `-`, `*` ou `/`.
3. Cliquez sur les chiffres du second nombre.
4. Cliquez sur `=` : le résultat s'affiche à l'écran.
5. Cliquez sur `C` pour effacer l'écran.

Le résultat reste affiché à l'écran : vous pouvez enchaîner une nouvelle opération à partir
de celui-ci (p. ex. `10.0` puis `+`, `5`, `=`).

### Exemples

| Expression | Résultat attendu |
|------------|------------------|
| `7+5`      | `12.0`           |
| `9-4`      | `5.0`            |
| `6*4`      | `24.0`           |
| `6/4`      | `1.5`            |

Les résultats sont toujours affichés en nombres décimaux (`float`).

### Messages d'erreur

| Message affiché                     | Cause |
|-------------------------------------|-------|
| `Error: empty expression`           | On a cliqué sur `=` avec un écran vide. |
| `Error: only one operator is allowed` | L'expression contient plus d'un opérateur (p. ex. `1+2+3`). |
| `Error: invalid expression format`  | Pas d'opérateur, ou opérateur au début/à la fin (p. ex. `5+`, `-3`). |
| `Error: operands must be numbers`   | Un opérande n'est pas un nombre valide (p. ex. `1.2.3+4`). |
| `Error: ...` (division)             | Division par zéro (p. ex. `5/0`). |

## Tests

Les tests automatisés se trouvent dans le répertoire [`tests/`](tests/) et utilisent
[pytest](https://docs.pytest.org/). Voir [`tests/README.md`](tests/README.md) pour le détail
de ce qui est couvert.

Depuis la racine du dépôt, avec l'environnement virtuel activé :

```bash
python -m pytest                     # exécuter toute la suite
python -m pytest -v                  # afficher le nom et le statut de chaque test
python -m pytest tests/test_operators.py   # exécuter un seul fichier
python -m pytest -k subtract         # exécuter les tests dont le nom contient « subtract »
```

Tous les tests doivent passer avant qu'une pull request soit fusionnée dans `main`.

## Flux de contribution

La branche `main` contient toujours une version stable dont **tous les tests passent**.
On ne pousse jamais directement sur `main` : tout changement passe par une issue, une
branche et une pull request.

### 1. Ouvrir une issue

Chaque bogue ou fonctionnalité commence par une [issue GitHub](https://github.com/elou14040/TP3_LOG3000/issues) :

- **Titre** court et précis (p. ex. « `subtract` inverse les opérandes »).
- **Description** : comportement observé et comportement attendu.
- **Étapes de reproduction** ou test en échec (commande et sortie de pytest).
- **Assignation** à un membre de l'équipe et étiquette (`bug`, `documentation`, `enhancement`).

### 2. Créer une branche

Une branche par issue, créée à partir d'un `main` à jour :

```bash
git checkout main
git pull origin main
git checkout -b fix/12-subtract-operandes
```

Convention de nommage : `<type>/<numéro-issue>-<description-courte>`

| Préfixe  | Usage |
|----------|-------|
| `fix/`   | Correction de bogue |
| `feat/`  | Nouvelle fonctionnalité |
| `docs/`  | Documentation |
| `test/`  | Ajout ou modification de tests |

### 3. Commiter

- Des commits petits et ciblés, un sujet par commit.
- Message à l'impératif qui explique **ce qui** change et **pourquoi**, avec la référence de
  l'issue :

  ```
  Corriger subtract pour retourner a - b (#12)

  La fonction retournait b - a, ce qui inversait le signe du résultat.
  Le test test_subtract passe maintenant.
  ```

- Avant de pousser, lancer `python -m pytest` : tous les tests doivent passer.

```bash
git push -u origin fix/12-subtract-operandes
```

### 4. Ouvrir une pull request

- Base : `main`. Titre clair et description qui indique le changement, la façon de le
  vérifier, et `Closes #12` pour fermer automatiquement l'issue à la fusion.
- Au moins **un autre membre** de l'équipe relit la PR et l'approuve.
- La PR est fusionnée seulement après l'approbation et si tous les tests passent ; la branche
  est ensuite supprimée.
