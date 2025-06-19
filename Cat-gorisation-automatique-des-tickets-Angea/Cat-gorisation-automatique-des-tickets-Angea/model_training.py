import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, accuracy_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay
)

# ✅ Générer des tickets d'exemple
def create_ticket_csv(file_path="tickets_annotes.csv"):
    print("📄 Création d'un fichier tickets_annotes.csv d'exemple...")

    categories = [
        "Support utilisateur", "Problème matériel", "Problème logiciel", "Accès / authentification",
        "Réinitialisation mot de passe", "Création de compte", "Droit d’accès réseau", "Sécurité informatique",
        "Demande de matériel", "Défaillance serveur", "Mise à jour système", "Sauvegarde / Restauration",
        "Bug applicatif", "Incident réseau", "Configuration poste de travail", "Problème d’imprimante",
        "Problème d’écran", "VPN / Télétravail", "Problème de connexion Wi-Fi", "Dysfonctionnement email",
        "Phishing / Spam", "Installation de logiciel", "Problème avec messagerie", "Requête base de données",
        "Déploiement d’application", "Erreur de script", "Demande de formation", "Support bureautique",
        "Problème de lenteur", "Migration de données", "Incident de production", "Monitoring / Supervision",
        "Configuration pare-feu", "Test utilisateur", "Gestion des licences", "Ticket de relance fournisseur",
        "Vérification conformité RGPD", "Intégration API", "Ticket de maintenance planifiée",
        "Problème de sauvegarde automatique", "Problème d’authentification SSO", "Incident sur cloud",
        "Audit de sécurité", "Vérification logs système", "Anomalie de performance", "Gestion de projet",
        "Développement web", "Déploiement CI/CD", "Ticket de test QA", "Gestion du parc informatique"
    ]

    data = []
    for cat in categories:
        for i in range(3):
            titre = f"Ticket {i+1} - {cat}"
            description = f"Description simulée pour un cas de {cat.lower()}."
            texte = f"{titre}. {description}"
            data.append({"texte": texte, "catégorie": cat})

    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"✅ Nouveau fichier généré avec {len(df)} tickets.")

# ✅ Comparaison de modèles
def compare_models(X_train, X_test, y_train, y_test):
    models = {
        "SVM": SVC(kernel="linear", C=1),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000)
    }

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")
        results[name] = {"model": model, "accuracy": acc, "f1": f1}

        print(f"\n✅ {name} : Accuracy = {acc:.4f} | F1-score = {f1:.4f}")
        print(classification_report(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)

        # ✅ Amélioration de la lisibilité
        fig, ax = plt.subplots(figsize=(16, 16))  # Taille de la figure
        disp.plot(ax=ax, xticks_rotation=90, cmap=plt.cm.Blues)  # Rotation des labels
        plt.title(f"Matrice de confusion - {name}")
        plt.tight_layout()

        filename = f"confusion_matrix_{name.replace(' ', '_')}.png"
        plt.savefig(filename, dpi=300)
        print(f"🖼️ Matrice de confusion sauvegardée sous {filename}")
        plt.show()
        plt.close()

    best_name, best_info = max(results.items(), key=lambda item: item[1]["f1"])
    print(f"\n🏆 Meilleur modèle : {best_name} (F1-score : {best_info['f1']:.4f})")

    model_filename = f"model_{best_name.replace(' ', '_').lower()}.pkl"
    joblib.dump(best_info["model"], model_filename)
    print(f"📦 Modèle sauvegardé sous {model_filename}")

    return best_info["model"]

# ✅ Entraînement global
def train_model(csv_file="tickets_annotes.csv"):
    if os.path.exists(csv_file):
        os.remove(csv_file)
    create_ticket_csv(csv_file)

    df = pd.read_csv(csv_file)

    if "texte" not in df.columns or "catégorie" not in df.columns:
        raise ValueError("❌ Le fichier doit contenir les colonnes 'texte' et 'catégorie'.")

    X = df["texte"]
    y = df["catégorie"]

    print("\n📊 Nombre d'exemples par classe dans l'ensemble complet :")
    print(y.value_counts())

    vectorizer = TfidfVectorizer()
    X_vect = vectorizer.fit_transform(X)

    n_classes = len(y.unique())
    min_test_size = n_classes / len(y)
    test_size = max(0.2, min_test_size)

    print(f"\n🔎 Utilisation de test_size = {test_size:.2f}")
    X_train, X_test, y_train, y_test = train_test_split(
        X_vect, y, test_size=test_size, random_state=42, stratify=y
    )

    print("\n📊 Nombre d'exemples par classe dans l'ensemble test :")
    print(y_test.value_counts())

    best_model = compare_models(X_train, X_test, y_train, y_test)

    joblib.dump(vectorizer, "vectorizer_tfidf.pkl")
    print("✅ Vectoriseur sauvegardé sous vectorizer_tfidf.pkl")

# 🚀 Lancer l'entraînement
if __name__ == "__main__":
    train_model()
