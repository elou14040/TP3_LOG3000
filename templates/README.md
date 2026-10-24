# `templates/` – Interface utilisateur

## Raison d'être

Ce répertoire contient les gabarits HTML rendus par Flask. C'est ici que se trouve
l'interface de la calculatrice : l'écran, les boutons et le petit script qui construit
l'expression avant de l'envoyer au serveur.

Flask cherche automatiquement les gabarits dans un dossier nommé `templates/` à côté de
`app.py` : **ce nom ne doit pas être changé**.

## Fichiers

| Fichier      | Responsabilité |
|--------------|----------------|
| `index.html` | Page unique de la calculatrice (route `/`). Affiche l'écran (`#display`) et une grille de 16 boutons. Contient deux fonctions JavaScript : `appendToDisplay(value)` ajoute un caractère à l'écran, `clearDisplay()` le vide. La variable `showingResult`, initialisée par Jinja, indique si l'écran affiche un résultat ou une erreur renvoyés par le serveur. |

## Fonctionnement

1. L'utilisateur clique sur des chiffres et un opérateur : le JavaScript ajoute les caractères
   dans le champ `display` (en lecture seule, donc pas de saisie au clavier).
2. Le bouton `=` soumet le formulaire en `POST` vers `/`.
3. `app.py` lit le champ `display`, calcule le résultat et renvoie la même page.
4. Le résultat (ou un message `Error: ...`) est injecté dans l'écran par la variable
   Jinja `{{ result }}`, et `showingResult` passe à vrai. Un opérateur tapé ensuite s'ajoute au
   résultat (enchaînement) ; un chiffre remplace l'écran et commence un nouveau calcul.

## Dépendances et hypothèses

- **Jinja2** (installé avec Flask) : moteur de gabarits utilisé pour `{{ result }}` et
  `{{ url_for('static', filename='style.css') }}`.
- **`static/style.css`** : feuille de style chargée par la page (voir [`../static/README.md`](../static/README.md)).
- **Contrat avec le backend** : le champ du formulaire doit s'appeler `display`, et
  l'expression doit avoir la forme `nombre opérateur nombre` (un seul opérateur parmi
  `+ - * /`), sinon le serveur renvoie une erreur.
- JavaScript doit être activé dans le navigateur, sinon les boutons ne remplissent pas l'écran.
- Aucune bibliothèque JavaScript externe n'est utilisée.
