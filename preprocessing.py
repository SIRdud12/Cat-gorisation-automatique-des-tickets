import pandas as pd
import spacy
import string
import os
from jira import JIRA

nlp = spacy.load("fr_core_news_sm")

def clean_text(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if token.is_alpha and not token.is_stop and token.lemma_ not in string.punctuation
    ]
    return " ".join(tokens)

def create_example_csv(file_name="tickets.csv"):
    if not os.path.exists(file_name):
        print(" Création d'un fichier tickets.csv d'exemple...")
        exemples = {
            "id": [1, 2, 3, 4],
            "texte": [
                "Erreur de connexion à la base de données.",
                "Impossible d’imprimer le document depuis l’application.",
                "Problème de mot de passe oublié pour l’utilisateur.",
                "La page reste bloquée après avoir cliqué sur envoyer."
            ]
        }
        df_exemple = pd.DataFrame(exemples)
        df_exemple.to_csv(file_name, index=False)
        print(f"✅ Fichier exemple créé : {file_name}")


def preprocess_csv(input_file="tickets.csv", output_file="cleaned_tickets.csv"):
    create_example_csv(input_file)
    df = pd.read_csv(input_file)
    if 'texte' not in df.columns:
        raise ValueError("Le fichier doit contenir une colonne 'texte'.")
    df["texte_nettoye"] = df["texte"].astype(str).apply(clean_text)
    df.to_csv(output_file, index=False)
    print(f"✅ Fichier prétraité sauvegardé : {output_file}")

def preprocess_ticket_jira(ticket_key, output_file="cleaned_ticket_jira.csv"):
    jira = JIRA(
        server="https://angearenza.atlassian.net",
        basic_auth=("angearenza08@gmail.com", "ATATT3xFfGF0gv1yxteUharRGs_n0Zn0VBQ_A3zXA0Zfqxqt_dzrkoTW_5f4qgShcz-IuW3r7gSSCFvVxyCt2yI7VGmfzRbohCeuFXYIRP7GbXiMwxmRLSRSWcgRzXdLY8GfdXdc1mWS6DoHFk8GI7btxgof8wuvp_JlUiGikgDJzEzPaag-9f8=46D1BA05")
    )
    issue = jira.issue(ticket_key)
    texte = issue.fields.summary + " " + (issue.fields.description or "")
    texte_nettoye = clean_text(texte)
    df = pd.DataFrame([{"ticket": ticket_key, "texte": texte, "texte_nettoye": texte_nettoye}])
    df.to_csv(output_file, index=False)
    print(f"✅ Ticket JIRA {ticket_key} prétraité et sauvegardé dans {output_file}")

if __name__ == "__main__":
    preprocess_csv("tickets.csv", "cleaned_tickets.csv")
    

