import streamlit as st
import pandas as pd
import os
from jira import JIRA
import uuid

# Config
st.set_page_config(page_title="Zendesk Dashboard", layout="wide")

# Config Jira
JIRA_URL = "https://angearenza.atlassian.net"
EMAIL = "angearenza08@gmail.com"
API_TOKEN = "ATATT3xFfGF00Mss6chbnJymPkgWk8ULg7JFntSVbYaq6dZmrgmgz-UkDTJoErLLDg16jGJbdu557JCVfER5MjtaQKBKj3kHsD-03F7JrP-wPNLnQ5dNbXK_7NjInkbUP_TOdKFcnay8vx0ZQhVmBIeSX1tzf67rnNOBk1SDdeFdGsYzOVe4S34=066C7B9A"

# Connexion Jira
jira = JIRA(server=JIRA_URL, basic_auth=(EMAIL, API_TOKEN))

# Données initiales
if "tickets" not in st.session_state:
    if os.path.exists("tickets.csv"):
        st.session_state["tickets"] = pd.read_csv("tickets.csv")
    else:
        st.session_state["tickets"] = pd.DataFrame(columns=[
            "ID", "Projet Jira", "Jira Key", "Type de ticket", "Titre", "Description",
            "Client", "Priorité", "Statut", "Assigné à"
        ])

if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Dashboard"

if "selected_ticket" not in st.session_state:
    st.session_state["selected_ticket"] = None

# CSS : clean sidebar (inchangé)
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

# Fonctions badges
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
if page == "🏠 Dashboard":
    st.title("🚀 Tableau de bord Jira - Vue globale")

    try:
        projets = jira.projects()
        nb_projets = len(projets)

        # CSS + amélioré (lisibilité ++)
        st.markdown("""
            <style>
            .big-card {
                background: linear-gradient(135deg, rgba(27,92,240,1), rgba(106,17,203,1));
                color: white;
                border-radius: 18px;
                padding: 24px;
                font-size: 2rem;
                font-weight: bold;
                text-align: center;
                margin-bottom: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            .kpi-card {
                background: #202642;
                border: 1px solid #3b3f58;
                border-radius: 20px;
                padding: 20px;
                text-align: center;
                color: #ffffff;
                box-shadow: 0 8px 24px rgba(0,0,0,0.4);
            }
            .kpi-title {
                font-size: 1.1rem;
                color: #b0b3c7;
                margin-bottom: 10px;
            }
            .kpi-value {
                font-size: 2.8rem;
                font-weight: bold;
                color: #ffffff;
            }
            .ticket-card {
                background: #282c44;
                border-radius: 16px;
                padding: 18px 24px;
                margin-bottom: 14px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.3);
                color: #f5f5f5;
            }
            .ticket-card strong {
                font-size: 1.2rem;
                color: #00d4ff;
            }
            .ticket-card small {
                font-size: 0.95rem;
                color: #d0d0d0;
            }
            </style>
        """, unsafe_allow_html=True)

        # Big card nb projets
        st.markdown(f'<div class="big-card">📁 Nombre de projets Jira : {nb_projets}</div>', unsafe_allow_html=True)

        # Sélection projet
        liste_projets = [proj.key for proj in projets]
        selected_project = st.selectbox("📂 Sélectionnez un projet :", liste_projets)

        # Récup tickets
        jql_query = f'project = {selected_project} ORDER BY created DESC'
        issues = jira.search_issues(jql_query, maxResults=100)

        # KPI
        count_open = sum(1 for i in issues if i.fields.status.name.lower() in ["open", "à faire", "new", "en cours"])
        count_onhold = sum(1 for i in issues if "attente" in i.fields.status.name.lower() or "hold" in i.fields.status.name.lower())
        count_resolved = sum(1 for i in issues if i.fields.status.name.lower() in ["resolved", "done", "closed", "résolu", "terminé"])
        count_unassigned = sum(1 for i in issues if not i.fields.assignee)
        total_tickets = len(issues)
        count_recent = sum(1 for i in issues if pd.to_datetime(i.fields.created[:10]) >= pd.Timestamp.now() - pd.Timedelta(days=7))

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">🟢 Ouverts</div>
                <div class="kpi-value">{count_open}</div>
            </div>
        """, unsafe_allow_html=True)
        col2.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">⏳ En attente</div>
                <div class="kpi-value">{count_onhold}</div>
            </div>
        """, unsafe_allow_html=True)
        col3.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">✅ Résolus</div>
                <div class="kpi-value">{count_resolved}</div>
            </div>
        """, unsafe_allow_html=True)
        col4.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">🚫 Non assignés</div>
                <div class="kpi-value">{count_unassigned}</div>
            </div>
        """, unsafe_allow_html=True)
        col5.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">🆕 Créés cette semaine</div>
                <div class="kpi-value">{count_recent}</div>
            </div>
        """, unsafe_allow_html=True)
        col6.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">📊 Total</div>
                <div class="kpi-value">{total_tickets}</div>
            </div>
        """, unsafe_allow_html=True)

        # Répartition statuts
        st.markdown("---")
        st.subheader(f"📈 Répartition par statut dans {selected_project}")

        all_status = {}
        for i in issues:
            s = i.fields.status.name
            all_status[s] = all_status.get(s, 0) + 1

        if all_status:
            df_status = pd.DataFrame(list(all_status.items()), columns=["Statut", "Count"])

            import altair as alt
            pie_chart = alt.Chart(df_status).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Statut", type="nominal"),
                tooltip=["Statut", "Count"]
            ).properties(width=400, height=400, title="Répartition des tickets")
            st.altair_chart(pie_chart, use_container_width=True)
        else:
            st.info("Aucun ticket sur ce projet.")

        # Derniers tickets
        st.markdown("---")
        st.subheader(f"🗂️ Derniers tickets du projet {selected_project}")

        if issues:
            for issue in issues[:10]:
                f = issue.fields
                titre = f.summary
                statut = f.status.name
                assignee = f.assignee.displayName if f.assignee else "Non assigné"
                priorite = f.priority.name if f.priority else "Non défini"
                create_date = issue.fields.created[:10]
                update_date = issue.fields.updated[:10]
                issue_link = f"{JIRA_URL}/browse/{issue.key}"

                st.markdown(f"""
                    <div class="ticket-card">
                        <strong><a href="{issue_link}" target="_blank">{issue.key}</a></strong> | {titre} <br>
                        <small>📅 Créé le {create_date} | 🔄 Maj : {update_date} | 🏷️ {statut} | 🔥 {priorite} | 👤 {assignee}</small>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Aucun ticket à afficher.")

    except Exception as e:
        st.error(f"❌ Erreur lors de la récupération Jira : {e}")

elif page == "🎟️ Tickets":
    st.title("🎟️ Tickets Jira en direct")

    projet_jira = st.text_input("Clé du projet Jira (ex: KAN)")

    if projet_jira:
        try:
            jql_query = f'project = {projet_jira} AND status != Closed ORDER BY created DESC'
            issues = jira.search_issues(jql_query, maxResults=50)

            if not issues:
                st.info(f"Aucun ticket ouvert trouvé pour le projet {projet_jira}.")
            else:
                st.markdown("""
                    <style>
                    .ticket-card {
                        background: #ffffff;
                        border-radius: 12px;
                        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                        padding: 20px;
                        margin-bottom: 20px;
                        transition: transform 0.2s ease, box-shadow 0.2s ease;
                    }
                    .ticket-card:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
                    }
                    .ticket-header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 12px;
                    }
                    .ticket-title {
                        font-size: 1.3rem;
                        font-weight: 700;
                        color: #1b5cf0;
                        margin: 0;
                    }
                    .ticket-key {
                        font-weight: 600;
                        font-size: 1rem;
                        color: #555;
                        text-decoration: none;
                        background: #e6f0ff;
                        padding: 6px 12px;
                        border-radius: 8px;
                        transition: background-color 0.2s ease;
                    }
                    .ticket-key:hover {
                        background: #c3dbff;
                    }
                    .ticket-description {
                        font-size: 0.95rem;
                        color: #444;
                        margin: 10px 0 15px 0;
                        white-space: pre-wrap;
                    }
                    .ticket-meta {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 15px;
                        font-size: 0.9rem;
                        color: #666;
                    }
                    .meta-item {
                        display: flex;
                        align-items: center;
                        gap: 6px;
                    }
                    .badge {
                        padding: 4px 10px;
                        border-radius: 14px;
                        font-size: 0.85rem;
                        font-weight: 600;
                        color: white;
                        display: inline-block;
                    }
                    .badge-priority-urgent { background-color: #e74c3c; }
                    .badge-priority-medium { background-color: #f39c12; }
                    .badge-priority-low { background-color: #2ecc71; }
                    .badge-status-open { background-color: #3498db; }
                    .badge-status-onhold { background-color: #9b59b6; }
                    .badge-status-resolved { background-color: #95a5a6; }
                    </style>
                """, unsafe_allow_html=True)

                def priority_badge(p):
                    p_lower = p.lower()
                    if "urgent" in p_lower:
                        return '<span class="badge badge-priority-urgent">Urgent</span>'
                    elif "moyenne" in p_lower or "medium" in p_lower:
                        return '<span class="badge badge-priority-medium">Moyenne</span>'
                    elif "basse" in p_lower or "low" in p_lower:
                        return '<span class="badge badge-priority-low">Basse</span>'
                    else:
                        return f'<span class="badge" style="background:#999;">{p}</span>'

                def status_badge(s):
                    s_lower = s.lower()
                    if "open" in s_lower:
                        return '<span class="badge badge-status-open">Open</span>'
                    elif "hold" in s_lower:
                        return '<span class="badge badge-status-onhold">On hold</span>'
                    elif "resolved" in s_lower:
                        return '<span class="badge badge-status-resolved">Resolved</span>'
                    else:
                        return f'<span class="badge" style="background:#999;">{s}</span>'

                for issue in issues:
                    f = issue.fields
                    titre = f.summary
                    desc = f.description or "Pas de description."
                    type_ticket = f.issuetype.name
                    priorite = f.priority.name if f.priority else "Non défini"
                    statut = f.status.name
                    assignee = f.assignee.displayName if f.assignee else "Non assigné"
                    # Adapt client si champ custom présent, sinon mettre 'N/A'
                    client = getattr(f, 'customfield_XXXXX', 'N/A')

                    st.markdown(f"""
                        <div class="ticket-card">
                            <div class="ticket-header">
                                <h2 class="ticket-title">{titre}</h2>
                                <a class="ticket-key" href="{JIRA_URL}/browse/{issue.key}" target="_blank">{issue.key}</a>
                            </div>
                            <div class="ticket-description">{desc}</div>
                            <div class="ticket-meta">
                                <div class="meta-item"><strong>Type :</strong> {type_ticket}</div>
                                <div class="meta-item"><strong>Priorité :</strong> {priority_badge(priorite)}</div>
                                <div class="meta-item"><strong>Statut :</strong> {status_badge(statut)}</div>
                                <div class="meta-item"><strong>Assigné à :</strong> {assignee}</div>
                                <div class="meta-item"><strong>Client :</strong> {client}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erreur lors de la récupération des tickets Jira : {e}")
    else:
        st.info("Merci de saisir une clé de projet Jira pour afficher les tickets.")

# Page Nouveau Ticket
elif page == "➕ Nouveau Ticket":
    st.title("📝 Créer un nouveau ticket")

    with st.form("new_ticket_form"):
        projet_jira = st.text_input("Projet Jira (clé, ex: KAN)")
        
        # Aller chercher dynamiquement les types de tickets valides
        issuetype_names = []
        if projet_jira:
            try:
                issuetypes = jira.issue_types_for_project(projet_jira)
                issuetype_names = [it.name for it in issuetypes]
            except Exception as e:
                st.warning(f"Impossible de récupérer les types de ticket : {e}")

        if issuetype_names:
            type_ticket = st.selectbox("Type de ticket", issuetype_names)
        else:
            type_ticket = st.text_input("Type de ticket (ex: Epic, Incident, Support...)")
        
        titre = st.text_input("Titre du ticket")
        description = st.text_area("Description du ticket")
        client = st.text_input("Nom du client")
        priorite = st.selectbox("Priorité", ["Urgent", "Moyenne", "Basse"])
        statut = st.selectbox("Statut", ["Open", "On hold", "Resolved"])
        assignee = st.text_input("Assigné à (username Jira)")
        
        submitted = st.form_submit_button("✅ Enregistrer et envoyer à Jira")

        if submitted:
            try:
                # Construction du dictionnaire Jira
                issue_dict = {
                    'project': {'key': projet_jira},
                    'summary': titre,
                    'description': description,
                    'issuetype': {'name': type_ticket},
                }

                if assignee:
                    issue_dict['assignee'] = {'name': assignee}

                # Création du ticket sur Jira
                issue = jira.create_issue(fields=issue_dict)
                st.success(f"✅ Ticket créé sur Jira avec la clé : {issue.key}")

                # Ajout au CSV + session state
                ticket_id = str(uuid.uuid4())
                new_ticket = {
                    "ID": ticket_id,
                    "Projet Jira": projet_jira,
                    "Type de ticket": type_ticket,
                    "Titre": titre,
                    "Description": description,
                    "Client": client,
                    "Priorité": priorite,
                    "Statut": statut,
                    "Assigné à": assignee,
                    "Clé Jira": issue.key
                }

                st.session_state["tickets"] = pd.concat([st.session_state["tickets"], pd.DataFrame([new_ticket])], ignore_index=True)
                st.session_state["tickets"].to_csv("tickets.csv", index=False)

            except Exception as e:
                st.error(f"❌ Erreur lors de la création du ticket Jira : {e}")

# Contacts
elif page == "📇 Contacts":
    st.title("👥 Contacts clients")
    st.table([
        {"Nom": "Emily Garcia", "Email": "emily@acme.com", "Téléphone": "+144..."},
        {"Nom": "Bob Tree", "Email": "bob@freshdesk.com", "Téléphone": "829..."},
        {"Nom": "Sarah James", "Email": "sarah@advanced.com", "Téléphone": "185..."},
    ])
