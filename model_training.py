import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import joblib
import os

def create_ticket_csv(file_path="tickets_annotes.csv"):
    if not os.path.exists(file_path):
        print("📄 Création d'un fichier tickets_annotes.csv d'exemple...")
        data = {
            "id": [1, 2, 3, 4, 5],
            "texte": [
                "Erreur de connexion à la base de données.",
                "Impossible d’imprimer le document depuis l’application.",
                "Mot de passe oublié pour l’utilisateur principal.",
                "Demande d’accès au dossier partagé du service RH.",
                "Alerte antivirus détectée sur le poste de travail."
            ],
            "catégorie": [
                "Réseau",
                "Support matériel",
                "Support utilisateur",
                "Accès / autorisations",
                "Sécurité informatique"
            ]
        }
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f"✅ Fichier créé : {file_path}")
    else:
        print(f" Fichier {file_path} déjà existant.")

def train_model(csv_file="tickets_annotes.csv"):
    create_ticket_csv(csv_file)  

    df = pd.read_csv(csv_file)

    if "texte" not in df.columns or "catégorie" not in df.columns:
        raise ValueError("❌ Le fichier doit contenir les colonnes 'texte' et 'catégorie'.")

    X = df["texte"]
    y = df["catégorie"]

   
    vectorizer = TfidfVectorizer()
    X_vect = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.2, random_state=42)

   
    model = LinearSVC()
    model.fit(X_train, y_train)

   
    y_pred = model.predict(X_test)
    print("\n Évaluation du modèle :")
    print(classification_report(y_test, y_pred))

  
    joblib.dump(model, "model_svm.pkl")
    joblib.dump(vectorizer, "vectorizer_tfidf.pkl")
    print("\n✅ Modèle et vectoriseur sauvegardés.")

if __name__ == "__main__":
    train_model()
