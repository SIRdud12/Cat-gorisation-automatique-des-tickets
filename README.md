# Cat-gorisation-automatique-des-tickets
SP - Catégorisation automatique des tickets
V

## `README.md`

markdown
# Dashboard Zendesk-like avec Classification Automatique des Tickets

Ce projet Streamlit permet de gérer et classifier automatiquement des tickets clients, dans une interface inspirée de Freshdesk/Zendesk. Il intègre un modèle de machine learning pour classer les tickets selon leur **catégorie** et **priorité**, avec une interface responsive, intuitive et stylisée.

---

##  Fonctionnalités

-  Dashboard style Zendesk
-  Classification automatique avec TF-IDF + modèle ML
-  Création de tickets
-  Liste des tickets avec prédictions
- Liste de contacts
- To-do intégrée
- Statistiques affichables (optionnel)

---

##  Prérequis

### 📌 1. Installer Python (>= 3.8 recommandé)

- **Windows** : https://www.python.org/downloads/windows/
- **macOS** : https://www.python.org/downloads/macos/

Assurez-vous de cocher l'option **"Add Python to PATH"** lors de l’installation sur Windows.

---

## Installation des dépendances

Ouvrir un terminal, se placer dans le dossier du projet, puis exécuter :

```bash
# Créer un environnement virtuel (optionnel mais recommandé)
python -m venv venv
# Activer l'environnement
# Windows :
venv\Scripts\activate
# macOS / Linux :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
````

---

##  `requirements.txt`

Crée un fichier `requirements.txt` avec le contenu suivant :

```
streamlit
pandas
scikit-learn
joblib
```

---

## ▶️ Lancer l'application

Depuis le terminal :

```bash
streamlit run app.py
```

Cela ouvrira automatiquement l'application dans votre navigateur :
➡️ [http://localhost:8501](http://localhost:8501)

---

## 📁 Structure du projet

```
.
├── app.py                     # Interface principale Streamlit
├── prediction.py              # Fonctions de prédiction catégorie/priorité
├── model_categorie.pkl        # Modèle ML entraîné pour la catégorie
├── model_priorite.pkl         # Modèle ML entraîné pour la priorité
├── vectorizer_tfidf.pkl       # Vectorizer TF-IDF
├── tickets.csv                # Tickets enregistrés localement
├── requirements.txt           # Dépendances Python
└── README.md                  # Documentation
```

---

##  Modèle Machine Learning

Les modèles ont été entraînés avec :

* `scikit-learn`
* Un `TfidfVectorizer`
* Deux modèles : `LogisticRegression` ou `RandomForest` (selon votre `model_training.py`)

> Tu peux les régénérer depuis `model_training.py` si tu modifies tes données.


