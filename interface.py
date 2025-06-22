import streamlit as st
from jira import JIRA

# Config Jira
JIRA_URL = "https://angearenza.atlassian.net"
EMAIL = "angearenza08@gmail.com"
API_TOKEN = "ATATT3xFfGF00Mss6chbnJymPkgWk8ULg7JFntSVbYaq6dZmrgmgz-UkDTJoErLLDg16jGJbdu557JCVfER5MjtaQKBKj3kHsD-03F7JrP-wPNLnQ5dNbXK_7NjInkbUP_TOdKFcnay8vx0ZQhVmBIeSX1tzf67rnNOBk1SDdeFdGsYzOVe4S34=066C7B9A"

jira = JIRA(server=JIRA_URL, basic_auth=(EMAIL, API_TOKEN))

# Style général
st.set_page_config(page_title="Panel Administrateur - Gestion Tickets", layout="wide")

st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1b1b2f, #162447);
    color: white;
}
.sidebar-icons {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    margin-top: 2rem;
}
button.sidebar-icon {
    font-size: 1.5rem !important;
    width: 3rem;
    height: 3rem;
    border-radius: 50%;
    border: none;
    background: #0f3460;
    color: white;
    cursor: pointer;
    transition: 0.2s;
}
button.sidebar-icon:hover {
    background: #e94560;
}
button.sidebar-icon.active {
    background: #53354a;
}

.big-title {
    font-size: 2.5rem;
    color: #00adb5;
    font-weight: bold;
    margin-bottom: 1rem;
}

.kpi {
    background: #222831;
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.kpi .number {
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.ticket-card {
    background: #0f3460;
    border-radius: 15px;
    padding: 20px;
    color: white;
    margin-bottom: 20px;
    box-shadow:
        0 0 5px #00fff5,
        0 0 10px #00fff5,
        0 0 20px #00fff5;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.ticket-card:hover {
    transform: translateY(-5px);
    box-shadow:
        0 0 10px #e94560,
        0 0 20px #e94560,
        0 0 30px #e94560;
}

.ticket-header {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
    color: #00fff5;
}

.ticket-meta {
    font-size: 0.9rem;
    color: #a0c4ff;
    margin-bottom: 10px;
}

.selectbox-small select {
    background: #162447;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
}

button.update-btn {
    background: #00adb5;
    color: #222831;
    border: none;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
button.update-btn:hover {
    background: #00fff5;
}
</style>
""", unsafe_allow_html=True)

# Sidebar nav
nav_icons = {
    "🏠": "Dashboard",
    "📋": "Tickets",
    "👥": "Clients",
     "🧑‍💻": "Utilisateurs"  
}

if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

st.sidebar.markdown('<div class="sidebar-icons">', unsafe_allow_html=True)
for emoji, label in nav_icons.items():
    selected = label
    is_active = st.session_state["page"] == selected
    if st.sidebar.button(emoji, key=f"nav-{label}"):
        st.session_state["page"] = selected
st.sidebar.markdown('</div>', unsafe_allow_html=True)

page = st.session_state["page"]

# --- PAGE DASHBOARD ---

if page == "Dashboard":
    st.markdown('<div class="big-title">📊 Tableau de Bord - Admin</div>', unsafe_allow_html=True)
    try:
        projets = jira.projects()
        nb_projets = len(projets)

        liste_projets = [proj.key for proj in projets]
        selected_project = st.selectbox("📂 Sélectionner un projet :", liste_projets)

        jql_query = f'project = {selected_project} ORDER BY created DESC'
        issues = jira.search_issues(jql_query, maxResults=100)

        # KPIs
        count_open = sum(1 for i in issues if i.fields.status.name.lower() in ["open", "à faire", "new", "en cours"])
        count_resolved = sum(1 for i in issues if i.fields.status.name.lower() in ["resolved", "done", "closed", "résolu", "terminé"])
        count_unassigned = sum(1 for i in issues if not i.fields.assignee)
        total_tickets = len(issues)

        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(f'<div class="kpi"><div class="number">{count_open}</div><div>Ouverts</div></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="kpi"><div class="number">{count_resolved}</div><div>Résolus</div></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="kpi"><div class="number">{count_unassigned}</div><div>Non assignés</div></div>', unsafe_allow_html=True)
        col4.markdown(f'<div class="kpi"><div class="number">{total_tickets}</div><div>Total tickets</div></div>', unsafe_allow_html=True)

        # Section "Nouvelles demandes"
        st.markdown("### 🆕 Dernières demandes utilisateurs")
        if issues:
            for issue in issues[:5]:
                f = issue.fields
                titre = f.summary
                statut = f.status.name
                priorite = f.priority.name if f.priority else "Non défini"
                assignee = f.assignee.displayName if f.assignee else "Non assigné"
                create_date = issue.fields.created[:10]
                issue_link = f"{JIRA_URL}/browse/{issue.key}"

                st.markdown(f"""
                    <div class="ticket-card">
                        <div class="ticket-header"><a href="{issue_link}" target="_blank" style="color:#00fff5;text-decoration:none;">{issue.key}</a> - {titre}</div>
                        <div class="ticket-meta">
                            📅 {create_date} | 🏷️ {statut} | 🔥 {priorite} | 👤 {assignee}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucune demande trouvée.")

    except Exception as e:
        st.error(f"Erreur lors de la récupération de Jira : {e}")

# --- PAGE TICKETS ---

elif page == "Tickets":
    st.markdown('<div class="big-title">📋 Tous les Tickets</div>', unsafe_allow_html=True)
    projet_jira = st.text_input("Nom du projet :", "")

    if projet_jira:
        try:
            jql_query = f'project = {projet_jira} ORDER BY created DESC'
            issues = jira.search_issues(jql_query, maxResults=50)

            if not issues:
                st.warning("Aucun ticket trouvé.")
            else:
                for issue in issues:
                    f = issue.fields
                    titre = f.summary
                    statut = f.status.name
                    assignee_display = f.assignee.displayName if f.assignee else "Non assigné"
                    priorite = f.priority.name if f.priority else "Non défini"
                    create_date = issue.fields.created[:10]
                    issue_link = f"{JIRA_URL}/browse/{issue.key}"
                    issue_key = issue.key

                    # Récupérer les transitions disponibles pour ce ticket (statuts possibles)
                    transitions = jira.transitions(issue)

                    # Récupérer les utilisateurs assignables dans ce projet
                    assignables = jira.search_assignable_users_for_projects('', projet_jira)
                    user_options = {user.displayName: user.accountId for user in assignables}

                    # Liste des statuts pour selectbox
                    status_options = [t['name'] for t in transitions]
                    if statut not in status_options:
                        status_options.insert(0, statut)  # garder l'ancien statut si non dans transitions

                    # Affichage card + formulaire de modif
                    with st.container():
                        st.markdown(f"""
                            <div class="ticket-card">
                                <div class="ticket-header"><a href="{issue_link}" target="_blank" style="color:#00fff5;text-decoration:none;">{issue_key}</a> - {titre}</div>
                                <div class="ticket-meta">
                                    📅 {create_date} | 🔥 {priorite}
                                </div>
                        """, unsafe_allow_html=True)

                        col1, col2 = st.columns(2)

                        with col1:
                            selected_statut = st.selectbox(
                                "Changer le statut",
                                options=status_options,
                                index=status_options.index(statut) if statut in status_options else 0,
                                key=f"status_{issue_key}"
                            )

                        with col2:
                            assign_display_names = ["Non assigné"] + list(user_options.keys())
                            default_index = assign_display_names.index(assignee_display) if assignee_display in assign_display_names else 0
                            selected_user_display = st.selectbox(
                                "Assigner à",
                                options=assign_display_names,
                                index=default_index,
                                key=f"assign_{issue_key}"
                            )

                        if st.button("💾 Appliquer les modifications", key=f"apply_{issue_key}"):
                            try:
                                # Modifier statut si changé
                                if selected_statut != statut:
                                    transition_id = next((t['id'] for t in transitions if t['name'] == selected_statut), None)
                                    if transition_id:
                                        jira.transition_issue(issue, transition_id)

                                # Modifier assigné si changé
                                if selected_user_display == "Non assigné":
                                    jira.assign_issue(issue, None)
                                else:
                                    account_id = user_options.get(selected_user_display)
                                    if account_id and any(u.accountId == account_id for u in assignables):
                                        jira.assign_issue(issue, account_id)
                                    else:
                                        st.error("Utilisateur non assignable sur ce projet.")
                                        continue  # Ne pas afficher succès

                                st.success(f"Ticket {issue_key} mis à jour avec succès.")
                            except Exception as e:
                                st.error(f"Erreur lors de la mise à jour : {e}")

                        st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erreur : {e}")

# --- PAGE CLIENTS ---

elif page == "Clients":
    st.markdown('<div class="big-title">👥 Gestion des clients</div>', unsafe_allow_html=True)
    st.table([
        {"Nom": "Emily Garcia", "Email": "emily@acme.com", "Téléphone": "+144..."},
        {"Nom": "Bob Tree", "Email": "bob@freshdesk.com", "Téléphone": "829..."},
        {"Nom": "Sarah James", "Email": "sarah@advanced.com", "Téléphone": "185..."},
    ])


# --- PAGE UTILISATEURS ---

elif page == "Utilisateurs":
    st.markdown('<div class="big-title">🧑‍💻 Gestion des Utilisateurs</div>', unsafe_allow_html=True)

    # Simuler une liste d'utilisateurs (à remplacer par une BDD plus tard)
    users = [
        {"Nom d'utilisateur": "admin", "Email": "admin@example.com", "Rôle": "admin"},
        {"Nom d'utilisateur": "support01", "Email": "support01@example.com", "Rôle": "support"},
        {"Nom d'utilisateur": "user123", "Email": "user123@example.com", "Rôle": "user"},
    ]

    st.markdown("### 📋 Liste des utilisateurs enregistrés")
    st.table(users)

    st.markdown("---")
    st.markdown("### ➕ Ajouter un nouvel utilisateur")

    new_username = st.text_input("Nom d'utilisateur")
    new_email = st.text_input("Email")
    new_role = st.selectbox("Rôle", options=["admin", "support", "user"])

    if st.button("Ajouter l'utilisateur"):
        # Ici normalement tu ferais un insert en BDD
        st.success(f"Utilisateur '{new_username}' ({new_role}) ajouté avec succès ! 🚀")

