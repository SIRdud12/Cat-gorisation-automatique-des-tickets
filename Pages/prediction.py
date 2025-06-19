import joblib

# Chargement des modèles une seule fois
_model_cat = joblib.load("model_categorie.pkl")
_model_prio = joblib.load("model_priorite.pkl")

def predict_category(text, vectorizer):
    X = vectorizer.transform([text])
    return _model_cat.predict(X)[0]

def predict_priority(text, vectorizer):
    X = vectorizer.transform([text])
    return _model_prio.predict(X)[0]
