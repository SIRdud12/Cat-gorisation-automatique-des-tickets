import streamlit as st
import pandas as pd
import os

# Config
st.set_page_config(page_title="Zendesk Dashboard", layout="wide")

# Données initiales
if "tickets" not in st.session_state:
    if os.path.exists("tickets.csv"):
        st.session_state["tickets"] = pd.read_csv("tickets.csv")
    else:
        st.session_state["tickets"] = pd.DataFrame(columns=["Titre", "Client", "Priorité", "Statut", "Assigné à"])

if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Dashboard"

if "selected_ticket" not in st.session_state:
    st.session_state["selected_ticket"] = None

# CSS : clean sidebar
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        width: 5rem !important;
        min-width: 5rem !important;
        max-width: 5rem !important;
        padding-top: 0.5rem;
    }
    .sidebar-icons {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.6rem;
        margin-top: 0.5rem;
    }
    button.sidebar-icon {
        font-size: 1.6rem !important;
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 10px;
        border: none;
        background: none;
        cursor: pointer;
        position: relative;
    }
    button.sidebar-icon:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        left: 140%;
        top: 50%;
        transform: translateY(-50%);
        background-color: #1b5cf0;
        color: white;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        white-space: nowrap;
        z-index: 99;
    }
    button.sidebar-icon.active {
        background-color: #e6f0ff;
    }
    .banner {
        background-color: #1b5cf0;
        padding: 1rem;
        color: white;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-weight: bold;
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
    </style>
""", unsafe_allow_html=True)

# (le reste du code reste inchangé)
...


# Sidebar
nav_icons = {
    "🏠": "Dashboard",
    "🎟️": "Tickets",
    "➕": "Nouveau Ticket",
    "📇": "Contacts"
}

st.sidebar.markdown('<div class="sidebar-icons">', unsafe_allow_html=True)
for emoji, label in nav_icons.items():
    selected = f"{emoji} {label}"
    is_active = st.session_state["page"] == selected
    if st.sidebar.button(emoji, key=f"nav-{label}"):
        st.session_state["page"] = selected
    st.markdown(f"""
        <script>
        const btn = window.parent.document.querySelector('button[data-testid="baseButton-element"][aria-label="{emoji}"]');
        if (btn) {{
            btn.className = "sidebar-icon {'active' if is_active else ''}";
            btn.setAttribute("data-tooltip", "{label}");
        }}
        </script>
    """, unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

page = st.session_state["page"]

# Dashboard
if page == "🏠 Dashboard":
    st.title("📊 Dashboard principal")

    st.markdown('<div class="banner">📢 Support clients across regions & time zones easily.</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown('<div class="kpi-box"><div class="kpi-title">Unresolved</div><div class="kpi-value">3</div></div>', unsafe_allow_html=True)
    col2.markdown('<div class="kpi-box"><div class="kpi-title">Open</div><div class="kpi-value">3</div></div>', unsafe_allow_html=True)
    col3.markdown('<div class="kpi-box"><div class="kpi-title">On hold</div><div class="kpi-value">0</div></div>', unsafe_allow_html=True)
    col4.markdown('<div class="kpi-box"><div class="kpi-title">Unassigned</div><div class="kpi-value">3</div></div>', unsafe_allow_html=True)

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

# Tickets avec filtres, badges et fiche ticket
elif page == "🎟️ Tickets":
    st.title("🎟️ Tickets enregistrés")

    df = st.session_state["tickets"]

    with st.expander("🔍 Filtres"):
        col1, col2, col3 = st.columns(3)
        with col1:
            filtre_prio = st.multiselect("Priorité", options=df["Priorité"].unique())
        with col2:
            filtre_statut = st.multiselect("Statut", options=df["Statut"].unique())
        with col3:
            filtre_client = st.multiselect("Client", options=df["Client"].unique())

    if filtre_prio:
        df = df[df["Priorité"].isin(filtre_prio)]
    if filtre_statut:
        df = df[df["Statut"].isin(filtre_statut)]
    if filtre_client:
        df = df[df["Client"].isin(filtre_client)]

    def badge(text, color):
        return f'<span style="background-color:{color}; color:white; padding:2px 8px; border-radius:12px; font-size:0.8rem;">{text}</span>'

    def badge_priorite(p):
        return {
            "Urgent": badge("Urgent", "#e74c3c"),
            "Moyenne": badge("Moyenne", "#f39c12"),
            "Basse": badge("Basse", "#2ecc71")
        }.get(p, p)

    def badge_statut(s):
        return {
            "Open": badge("Open", "#3498db"),
            "On hold": badge("On hold", "#9b59b6"),
            "Resolved": badge("Resolved", "#95a5a6")
        }.get(s, s)

    if not df.empty:
        for index, row in df.iterrows():
            if st.button(f"📂 {row['Titre']}", key=f"ticket-{index}"):
                st.session_state["selected_ticket"] = row

            if st.session_state["selected_ticket"] is not None and st.session_state["selected_ticket"]["Titre"] == row["Titre"]:
                with st.expander("📋 Détails du ticket", expanded=True):
                    st.markdown(f"**Client :** {row['Client']}")
                    st.markdown(f"**Priorité :** {badge_priorite(row['Priorité'])}", unsafe_allow_html=True)
                    st.markdown(f"**Statut :** {badge_statut(row['Statut'])}", unsafe_allow_html=True)
                    st.markdown(f"**Assigné à :** {row['Assigné à']}")
                    if st.button("❌ Fermer", key=f"close-{index}"):
                        st.session_state["selected_ticket"] = None
    else:
        st.info("Aucun ticket ne correspond aux filtres sélectionnés.")

# Nouveau ticket
elif page == "➕ Nouveau Ticket":
    st.title("📝 Créer un nouveau ticket")

    with st.form("new_ticket_form"):
        titre = st.text_input("Titre du ticket")
        client = st.text_input("Nom du client")
        priorite = st.selectbox("Priorité", ["Urgent", "Moyenne", "Basse"])
        statut = st.selectbox("Statut", ["Open", "On hold", "Resolved"])
        assignee = st.text_input("Assigné à")
        submitted = st.form_submit_button("✅ Enregistrer le ticket")

        if submitted:
            new_ticket = {
                "Titre": titre,
                "Client": client,
                "Priorité": priorite,
                "Statut": statut,
                "Assigné à": assignee
            }
            st.session_state["tickets"] = st.session_state["tickets"].append(new_ticket, ignore_index=True)
            st.session_state["tickets"].to_csv("tickets.csv", index=False)
            st.success("🎉 Ticket ajouté avec succès !")

# Contacts
elif page == "📇 Contacts":
    st.title("👥 Contacts clients")
    st.table([
        {"Nom": "Emily Garcia", "Email": "emily@acme.com", "Téléphone": "+144..."},
        {"Nom": "Bob Tree", "Email": "bob@freshdesk.com", "Téléphone": "829..."},
        {"Nom": "Sarah James", "Email": "sarah@advanced.com", "Téléphone": "185..."},
    ])
