from jira import JIRA

# === CONFIGURATION ===
JIRA_URL = "https://angearenza.atlassian.net"
EMAIL = "angearenza08@gmail.com"  
API_TOKEN = "ATATT3xFfGF0gv1yxteUharRGs_n0Zn0VBQ_A3zXA0Zfqxqt_dzrkoTW_5f4qgShcz-IuW3r7gSSCFvVxyCt2yI7VGmfzRbohCeuFXYIRP7GbXiMwxmRLSRSWcgRzXdLY8GfdXdc1mWS6DoHFk8GI7btxgof8wuvp_JlUiGikgDJzEzPaag-9f8=46D1BA05"  # ⚠️ secret !

# === Connexion à JIRA ===
jira = JIRA(server=JIRA_URL, basic_auth=(EMAIL, API_TOKEN))

# === Ticket cible ===
ticket_key = "KAN-1"

# === Lecture du ticket ===
issue = jira.issue(ticket_key)
description = issue.fields.summary + "\n" + (issue.fields.description or "")
print(f"\n📥 Texte extrait du ticket {ticket_key} :\n{description}")

# === Simulation de prédiction IA (exemple statique ici) ===
# Remplace cette ligne plus tard par ton vrai modèle
categorie_predite = "Support utilisateur"

# === Ajout de l'étiquette de catégorie ===
issue.fields.labels.append(categorie_predite.replace(" ", "_"))  # Les labels JIRA n'acceptent pas d'espaces
issue.update(fields={"labels": issue.fields.labels})

print(f"\n✅ Catégorie '{categorie_predite}' ajoutée dans les labels du ticket {ticket_key}.")
