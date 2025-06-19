import streamlit as st
import pandas as pd
import os

# Config page
st.set_page_config(page_title="Zendesk Dashboard", layout="wide")

# Initialisation
if "tickets" not in st.session_state:
    if os.path.exists("tickets.csv"):
        st.session_state["tickets"] = pd.read_csv("tickets.csv")
    else:
        st.session_state["tickets"] = pd.DataFrame(columns=["Titre", "Client", "Priorité", "Statut", "Assigné à"])

# Style CSS + Dark mode support
st.markdown("""
    <style>
    :root {
        --primary-color: #1b5cf0;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fc;
    }
    .kpi-box {
        background-color: #f4f6fb;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1rem;
    }
    .kpi-title { font-size: 0.9rem; color: #6b7a90; }
    .kpi-value { font-size: 2rem; font-weight: bold; }
    .card {
        background-color: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        height: 100%;
    }
    .banner {
        background-color: #1b5cf0;
        padding: 1rem;
        color: white;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar avec navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Freshdesk_logo_2022.svg/512px-Freshdesk_logo_2022.svg.png", width=180)
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Choisissez une page",
    ["🏠 Dashboard", "🎟️ Tickets", "➕ Nouveau Ticket", "📇 Contacts"],
    index=0
)

# === PAGE: Dashboard ===
if page == "🏠 Dashboard":
    st.title("📊 Dashboard principal")

    st.markdown('<div class="banner">📢 Support clients across regions & time zones easily.</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="kpi-box"><div class="kpi-title">Unresolved</div><div class="kpi-value">3</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-box"><div class="kpi-title">Open</div><div class="kpi-value">3</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-box"><div class="kpi-title">On hold</div><div class="kpi-value">0</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-box"><div class="kpi-title">Unassigned</div><div class="kpi-value">3</div></div>', unsafe_allow_html=True)

    col5, col6, col7 = st.columns(3)
    with col5:
        st.markdown('<div class="card"><b>📨 Undelivered emails</b><br><br><center>No undelivered emails</center><br><a href="#">View details</a></div>', unsafe_allow_html=True)
    with col6:
        st.markdown('<div class="card"><b>✅ To-do (4)</b>', unsafe_allow_html=True)
        st.checkbox("jbjb jhj")
        st.checkbox("ugyvivhj")
        st.checkbox("j jhbbvjh")
        st.checkbox(",n jb jb")
        st.markdown('</div>', unsafe_allow_html=True)
    with col7:
        st.markdown('<div class="card"><b>📋 Unresolved tickets</b><br><br>Customer Support (Open): <b>3</b><br><br><a href="#">View details</a></div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><b>📰 Recent Activity</b><br>Ulrich Eneli created article <a href="#">How to Fix Login Issues</a><br><small>📅 21 days ago</small></div>', unsafe_allow_html=True)

# === PAGE: Tickets ===
elif page == "🎟️ Tickets":
    st.title("🎫 Tickets enregistrés")

    import joblib
    from prediction import predict_category, predict_priority

    # Charger vectorizer et modèles
    try:
        vectorizer = joblib.load("vectorizer_tfidf.pkl")
    except FileNotFoundError:
        st.error("❌ Fichier 'vectorizer_tfidf.pkl' introuvable")

    if st.button("🎯 Classer automatiquement"):
        df = st.session_state["tickets"]

        df["Catégorie (auto)"] = df["Titre"].apply(lambda t: predict_category(t, vectorizer))
        df["Priorité (auto)"] = df["Titre"].apply(lambda t: predict_priority(t, vectorizer))

        st.session_state["tickets"] = df
        st.success("✅ Tickets classés automatiquement !")

    st.dataframe(st.session_state["tickets"], use_container_width=True)


# === PAGE: Nouveau Ticket ===
elif page == "➕ Nouveau Ticket":
    st.title("📝 Créer un nouveau ticket")

    with st.form("new_ticket_form"):
        titre = st.text_input("Titre du ticket")
        client = st.text_input("Nom du client")
        priorité = st.selectbox("Priorité", ["Urgent", "Moyenne", "Basse"])
        statut = st.selectbox("Statut", ["Open", "On hold", "Resolved"])
        assignee = st.text_input("Assigné à")
        submitted = st.form_submit_button("✅ Enregistrer le ticket")

        if submitted:
            new_ticket = {
                "Titre": titre,
                "Client": client,
                "Priorité": priorité,
                "Statut": statut,
                "Assigné à": assignee
            }
            st.session_state["tickets"] = st.session_state["tickets"].append(new_ticket, ignore_index=True)
            st.session_state["tickets"].to_csv("tickets.csv", index=False)
            st.success("🎉 Ticket ajouté avec succès !")

# === PAGE: Contacts ===
elif page == "📇 Contacts":
    st.title("👥 Contacts clients")
    st.table([
        {"Nom": "Emily Garcia", "Email": "emily@acme.com", "Téléphone": "+144..."},
        {"Nom": "Bob Tree", "Email": "bob@freshdesk.com", "Téléphone": "829..."},
        {"Nom": "Sarah James", "Email": "sarah@advanced.com", "Téléphone": "185..."},
    ])
