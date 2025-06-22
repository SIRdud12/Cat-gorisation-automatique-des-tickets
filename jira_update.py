from jira import JIRA
import joblib

JIRA_URL = "https://angearenza.atlassian.net"
EMAIL = "angearenza08@gmail.com" 
API_TOKEN = "ATATT3xFfGF0gv1yxteUharRGs_n0Zn0VBQ_A3zXA0Zfqxqt_dzrkoTW_5f4qgShcz-IuW3r7gSSCFvVxyCt2yI7VGmfzRbohCeuFXYIRP7GbXiMwxmRLSRSWcgRzXdLY8GfdXdc1mWS6DoHFk8GI7btxgof8wuvp_JlUiGikgDJzEzPaag-9f8=46D1BA05"  # ⚠️ secret !




jira = JIRA(server=JIRA_URL, basic_auth=(EMAIL, API_TOKEN))


model = joblib.load("model_svm.pkl")
vectorizer = joblib.load("vectorizer_tfidf.pkl")


ticket_key = "KAN-1"
issue = jira.issue(ticket_key)
texte = issue.fields.summary + " " + (issue.fields.description or "")


X_vect = vectorizer.transform([texte])
categorie = model.predict(X_vect)[0]
label = categorie.replace(" ", "_")


labels = issue.fields.labels
if label not in labels:
    labels.append(label)
    issue.update(fields={"labels": labels})
    print(f"✅ Label '{label}' ajouté au ticket {ticket_key}")
else:
    print(f"ℹ Le label '{label}' est déjà présent dans le ticket {ticket_key}")
