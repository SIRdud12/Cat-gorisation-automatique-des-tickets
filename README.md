# Cat-gorisation-automatique-des-tickets
SP - Catégorisation automatique des tickets

## 🎯 Objectif

Ce projet vise à automatiser la **classification des tickets IT** (incidents, demandes) en analysant leur contenu textuel (titre, description), en prédisant leur **catégorie** grâce à un **modèle de machine learning**, puis en **mettant à jour le ticket sur JIRA** avec la bonne étiquette.

---

## 📌 Technologies utilisées

- 🐍 Python 3.10+
- 📦 Bibliothèques : `pandas`, `spacy`, `scikit-learn`, `joblib`, `matplotlib`, `jira`
- 💡 NLP : spaCy (modèle `fr_core_news_sm`)
- 🤖 ML : SVM avec `TfidfVectorizer`
- 🛠️ API : JIRA Cloud REST API (via token personnel)

---

## ⚙️ Installation

### 1. Créer un environnement virtuel (facultatif mais conseillé)

```bash
python -m venv venv
venv\Scripts\activate   # Sur Windows
source venv/bin/activate # Sur MAcOS/Linux

```

### 2. Installer les dépendances

```bash
pip install pandas spacy scikit-learn joblib matplotlib jira
python -m spacy download fr_core_news_sm
```

---

## 📁 Structure du projet

```
SP-Ece/
├── preprocessing.py
├── model_training.py
├── prediction.py
├── jira_update.py
├── tickets.csv
├── tickets_annotes.csv
├── cleaned_tickets.csv
├── erreurs_model.csv
├── model_svm.pkl
├── vectorizer_tfidf.pkl
```

---

## 🚀 Étapes à suivre

### ✅ 1. Nettoyer les données
```bash
python preprocessing.py
```

### ✅ 2. Annoter les tickets
Compléter `tickets_annotes.csv`.

### ✅ 3. Entraîner le modèle IA
```bash
python model_training.py
```

### ✅ 4. Tester sur un ticket JIRA
```bash
python prediction.py
```

### ✅ 5. Mettre à jour automatiquement le ticket
```bash
python jira_update.py
```

---

## 🔐 Connexion à JIRA

## ## Utiliser dans ce projet ## ## 
Configurer dans `prediction.py` et `jira_update.py` :

```python  
JIRA_URL = "https://angearenza.atlassian.net"
EMAIL = "angearenza08@gmail.com"  
API_TOKEN =
"ATATT3xFfGF0gv1yxteUharRGs_n0Zn0VBQ_A3zXA0Zfqxqt_dzrkoTW_5f4qgShcz-IuW3r7gSSCFvVxyCt2yI7VGmfzRbohCeuFXYIRP7GbXiMwxmRLSRSWcgRzXdLY8GfdXdc1mWS6DoHFk8GI7btxgof8wuvp_JlUiGikgDJzEzPaag-9f8=46D1B05"  # ⚠️ secret !
ticket_key = "KAN-1"
```

Chaque utilisateur doit :

1. Créer un **compte Atlassian Cloud** (gratuit) :  
   https://id.atlassian.com/signup

2. Rejoindre le projet JIRA partagé (via invitation par le créateur)

3. Générer un **API Token personnel** ici :  
   https://id.atlassian.com/manage-profile/security/api-tokens

4. Mettre à jour son fichier local avec ses propres identifiants dans les fichiers `prediction.py` et `jira_update.py` :

```python
EMAIL = "votre.email@exemple.com"         # ← Votre compte Atlassian
API_TOKEN = "votre_token_personnel"       # ← Jamais partagé publiquement
JIRA_URL = "https://angearenza.atlassian.net"
ticket_key = "KAN-1"                      # ← Clé du ticket à tester




