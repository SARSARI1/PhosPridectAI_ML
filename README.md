# PhosPridectAI_FV
# Plateforme de Prédiction de Chiffre d'Affaires pour l'Office Chérifien des Phosphates (OCP)

Ce projet vise à développer une plateforme de prédiction du chiffre d'affaires pour l'Office Chérifien des Phosphates (OCP) en utilisant des techniques de Machine Learning. La plateforme inclut une interface web interactive développée avec Flask, permettant aux utilisateurs d'interagir avec les résultats de prédiction.

## Objectifs

L'objectif principal de ce projet est de développer un modèle de prédiction précis pour estimer le chiffre d'affaires futur de l'OCP, basé sur des données historiques. La plateforme permettra aux utilisateurs de :
- Prédire la quantité de phosphate
- Prédire le prix du phosphate
- Visualiser et explorer les prédictions de manière interactive

## Fonctionnalités

1. **Prédiction de Quantité de Phosphate :**
   - Utilisation de modèles de Machine Learning pour prédire la quantité de phosphate produite en fonction des nutriments et d'autres facteurs.

2. **Prédiction de Prix de Phosphate :**
   - Prédiction des prix futurs du phosphate basée sur des variables telles que le prix du diesel, le ratio prix phosphate/diesel, etc.

3. **Interface Web Interactive :**
   - Développée avec Flask, permettant aux utilisateurs de saisir des données, d'obtenir des prédictions et de visualiser les résultats de manière intuitive.

4. **Génération de Rapports PDF :**
   - Fonctionnalité permettant de générer des rapports PDF contenant les prédictions et les données pertinentes.

## Technologies Utilisées

- **Backend :**
  - Flask : Framework web pour la création de l'interface utilisateur.
  - SQLAlchemy : ORM pour la gestion des bases de données.
  - Pickle : Pour le chargement des modèles de Machine Learning.
  - Scikit-learn : Bibliothèque de Machine Learning utilisée pour la construction des modèles.

- **Frontend :**
  - HTML/CSS : Pour la création de l'interface utilisateur.
  - Matplotlib & Seaborn : Pour la visualisation des données.

- **Autres Outils :**
  - ReportLab : Pour la génération de rapports PDF.
  - Pandas : Pour la manipulation et l'analyse des données.

## Installation

1. **Cloner le dépôt :**
   ```sh
   git clone https://github.com/votre-utilisateur/ocp-prediction-platform.git
   cd ocp-prediction-platform
Créer et activer un environnement virtuel :

sh
Copier le code
python3 -m venv venv
source venv/bin/activate
Installer les dépendances :

sh
Copier le code
pip install -r requirements.txt
Configurer la base de données :

sh
Copier le code
flask db init
flask db migrate
flask db upgrade
Lancer l'application :

sh
Copier le code
flask run
Utilisation
Accédez à l'interface utilisateur via votre navigateur web à l'adresse http://localhost:5000.
Utilisez les différents formulaires pour prédire les quantités et les prix du phosphate.
Visualisez les résultats et générez des rapports PDF si nécessaire.
Contribuer
Les contributions sont les bienvenues ! Pour contribuer :

Fork le projet.
Créez une branche pour votre fonctionnalité (git checkout -b fonctionnalite-geniale).
Committez vos modifications (git commit -am 'Ajoute une fonctionnalité géniale').
Poussez vers la branche (git push origin fonctionnalite-geniale).
Ouvrez une Pull Request.
Contact
Pour toute question ou suggestion, veuillez contacter :

Nom: [Votre Nom]
Email: [votre.email@exemple.com]
GitHub: https://github.com/votre-utilisateur