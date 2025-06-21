import streamlit as st
import pandas as pd
from jira import JIRA
import joblib
import os

# Configuration
JIRA_URL = "https://angearenza.atlassian.net"
EMAIL = "angearenza08@gmail.com"
API_TOKEN = os.getenv("ATATT3xFfGF00Mss6chbnJymPkgWk8ULg7JFntSVbYaq6dZmrgmgz-UkDTJoErLLDg16jGJbdu557JCVfER5MjtaQKBKj3kHsD-03F7JrP-wPNLnQ5dNbXK_7NjInkbUP_TOdKFcnay8vx0ZQhVmBIeSX1tzf67rnNOBk1SDdeFdGsYzOVe4S34=066C7B9A")  # Plus sécurisé que dans le code en dur

# Modèle IA
_model_cat = joblib.load("model_svm.pkl")
_vectorizer = joblib.load("vectorizer_tfidf.pkl")

# Page config
st.set_page_config(page_title="Jira - Catégorisation IA", layout="wide")
st.title("🤖 Prédiction automatique des catégories Jira")

# Connexion à Jira
try:
    jira = JIRA(server=JIRA_URL, basic_auth=(EMAIL, API_TOKEN))
    st.success("✅ Connecté à Jira avec succès.")
except Exception as e:
    st.error(f"❌ Erreur de connexion à Jira : {e}")
    st.stop()

# Sélection du projet Jira
projets = jira.projects()
liste_projets = [proj.key for proj in projets]

selected_project = st.selectbox("Sélectionner un projet Jira :", liste_projets)

if st.button("📥 Charger les tickets du projet"):
    with st.spinner("🔄 Chargement des tickets..."):
        try:
            # Récupérer tous les tickets ouverts du projet
            jql = f'project = {selected_project} AND statusCategory != Done ORDER BY created DESC'
            issues = jira.search_issues(jql, maxResults=50)  # Limité à 50 pour l'exemple

            data = []

            for issue in issues:
                texte = (issue.fields.summary or "") + " " + (issue.fields.description or "")
                X_vect = _vectorizer.transform([texte])
                categorie = _model_cat.predict(X_vect)[0]

                data.append({
                    "Clé ticket": issue.key,
                    "Résumé": issue.fields.summary,
                    "Statut": issue.fields.status.name,
                    "Assigné à": issue.fields.assignee.displayName if issue.fields.assignee else "Non assigné",
                    "Catégorie prédite": categorie
                })

            df_resultats = pd.DataFrame(data)

            st.dataframe(df_resultats, use_container_width=True)

            # Bouton pour télécharger en CSV
            csv = df_resultats.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger les résultats (CSV)",
                data=csv,
                file_name=f"jira_tickets_{selected_project}.csv",
                mime='text/csv'
            )

        except Exception as e:
            st.error(f"❌ Erreur lors de la récupération des tickets : {e}")
