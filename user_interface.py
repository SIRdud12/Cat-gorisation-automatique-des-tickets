import streamlit as st
from jira import JIRA
import uuid

# Connexion Jira
JIRA_URL = "https://angearenza.atlassian.net"
EMAIL = "angearenza08@gmail.com"
API_TOKEN = "ATATT3xFfGF00Mss6chbnJymPkgWk8ULg7JFntSVbYaq6dZmrgmgz-UkDTJoErLLDg16jGJbdu557JCVfER5MjtaQKBKj3kHsD-03F7JrP-wPNLnQ5dNbXK_7NjInkbUP_TOdKFcnay8vx0ZQhVmBIeSX1tzf67rnNOBk1SDdeFdGsYzOVe4S34=066C7B9A"  # sécuriser en .env en vrai

jira = JIRA(server=JIRA_URL, basic_auth=(EMAIL, API_TOKEN))

# Mapping Service (affiché) → Projet Jira (clé)
projets_visibles = {
    "Support Informatique": "KAN",
    "Ressources Humaines": "RH",
    "Service Client": "SUPPORT"
}

# Page
st.set_page_config(page_title="Portail Support", layout="centered")
st.title("💬 Portail d'assistance")

st.markdown("""
Bienvenue sur notre centre de support. Veuillez remplir le formulaire ci-dessous, notre équipe vous répondra rapidement.  
""")

# Formulaire
with st.form("ticket_user_form"):
    service = st.selectbox("Quel service souhaitez-vous contacter ?", list(projets_visibles.keys()))
    titre = st.text_input("Objet de votre demande")
    description = st.text_area("Expliquez votre demande ou votre problème")
    priorite = st.radio("Niveau d'urgence", ["Haute", "Normale", "Basse"])
    nom_client = st.text_input("Votre nom complet")
    email_client = st.text_input("Votre adresse email")

    submitted = st.form_submit_button("📨 Envoyer la demande")

    if submitted:
        try:
            # Préparer ticket Jira
            projet_jira = projets_visibles[service]

            issue_dict = {
                'project': {'key': projet_jira},
                'summary': titre,
                'description': f"{description}\n\nClient: {nom_client}\nEmail: {email_client}",
                'issuetype': {'name': 'Incident'},  # ou "Service Request", selon config
            }

            # Créer ticket Jira
            issue = jira.create_issue(fields=issue_dict)
            st.success(f"✅ Votre demande a bien été envoyée ! Numéro de suivi : [{issue.key}]({JIRA_URL}/browse/{issue.key})")

        except Exception as e:
            st.error(f"❌ Une erreur est survenue lors de l'envoi : {e}")
