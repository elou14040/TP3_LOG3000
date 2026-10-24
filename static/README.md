# `static/` – Fichiers statiques

## Raison d'être

Ce répertoire contient les fichiers servis tels quels au navigateur, sans traitement par
le serveur (feuilles de style, et éventuellement images ou scripts à l'avenir).

Flask sert automatiquement le contenu de `static/` sous l'URL `/static/...` : **ce nom ne
doit pas être changé**.

## Fichiers

| Fichier     | Responsabilité |
|-------------|----------------|
| `style.css` | Apparence de la calculatrice : mise en page centrée, thème sombre, écran aligné à droite, grille de boutons 4 × 4 et couleur orange pour les opérateurs. |

## Principaux sélecteurs CSS

| Sélecteur     | Élément stylé |
|---------------|---------------|
| `body`        | Centre la calculatrice dans la fenêtre. |
| `.calculator` | Conteneur principal (fond sombre, coins arrondis, largeur max. 600 px). |
| `#display`    | Écran de la calculatrice. |
| `.buttons`    | Grille de 4 colonnes contenant les boutons. |
| `.btn`        | Style de base de tous les boutons. |
| `.operator`   | Variante orange pour `+ - * / =`. |

## Dépendances et hypothèses

- La feuille est chargée par [`templates/index.html`](../templates/README.md) via
  `url_for('static', filename='style.css')`.
- Les sélecteurs dépendent de la structure HTML : l'identifiant `display` et les classes
  `calculator`, `buttons`, `btn` et `operator` doivent rester synchronisés avec `index.html`.
- `.operator` est déclaré **après** `.btn` : l'ordre compte, car les deux règles ont la même
  spécificité et c'est la dernière qui fixe la couleur.
- Aucun préprocesseur (Sass, etc.) ni cadriciel CSS : du CSS pur, compatible avec les
  navigateurs modernes (utilise CSS Grid et Flexbox).
