"""
CSS global de l'application — injecté une seule fois au démarrage.
"""

CSS = """
<style>
html, body, .stApp, .stApp > * {
    background-color: #141920 !important;
    color: #d1dce8;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
.stApp > footer, footer,
div[data-testid="stBottom"],
div[data-testid="stBottom"] > * {
    background-color: #141920 !important;
    border-top: none !important;
    box-shadow: none !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
    border-right: 1px solid #1e2630 !important;
}
section[data-testid="stSidebar"] * { color: #8899aa !important; }
section[data-testid="stSidebar"] .sidebar-title {
    font-size: 1.15rem; font-weight: 700;
    color: #4ef2d2 !important; display: block; margin-bottom: 18px;
}
div[data-baseweb="slider"] [role="slider"] {
    background-color: #4ef2d2 !important; border-color: #4ef2d2 !important;
}
div[data-baseweb="slider"] div[data-testid="stSliderTrackActive"] {
    background-color: #4ef2d2 !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    background-color: #161c24 !important; border-color: #2a3444 !important; color: #cbd5e1 !important;
}
section[data-testid="stSidebar"] textarea {
    background-color: #161c24 !important; border: 1px solid #2a3444 !important;
    color: #cbd5e1 !important; border-radius: 8px !important;
}
section[data-testid="stSidebar"] button {
    background-color: #1f2c3d !important; color: #e05a5a !important;
    border: 1px solid #e05a5a44 !important; border-radius: 8px !important; font-weight: 600 !important;
}
section[data-testid="stSidebar"] button:hover {
    background-color: #2b1f1f !important; border-color: #e05a5a !important;
}

/* ── Layout ── */
.block-container {
    max-width: 920px !important;
    padding: 2rem 1rem 5rem 1rem !important;
    margin: 0 auto !important;
}

/* ── Header ── */
.chat-header { text-align: center; padding: 0 0 18px 0; }
.chat-header .robot-icon {
    font-size: 3.2rem; display: block; margin-bottom: 4px;
    filter: drop-shadow(0 0 12px rgba(78,242,210,0.5));
}
.chat-header h1 {
    font-size: 2.5rem !important; font-weight: 900 !important;
    color: #4ef2d2 !important; text-transform: uppercase; letter-spacing: 3px;
    text-shadow: 0 0 18px rgba(78,242,210,0.35), 0 0 40px rgba(78,242,210,0.15);
    margin: 0 0 6px 0 !important; line-height: 1.1;
}
.chat-header .caption { font-size: 0.85rem; color: #4a5b6f; }
.chat-header .caption code {
    background: #1e2a38; color: #4ef2d2;
    padding: 1px 7px; border-radius: 4px; font-size: 0.82rem;
}

/* ── Tabs ── */
div[data-testid="stTabs"] button {
    color: #8899aa !important; font-weight: 600;
    border-radius: 8px 8px 0 0 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #4ef2d2 !important;
    border-bottom: 2px solid #4ef2d2 !important;
}

/* ── Bulles chat ── */
.msg-row { display: flex; align-items: flex-start; gap: 10px; margin: 10px 0; }
.msg-row.user { flex-direction: row-reverse; }
.avatar {
    width: 38px; height: 38px; flex-shrink: 0;
    background: radial-gradient(circle, #1a3a2e 0%, #0d1f17 100%);
    border: 1.5px solid rgba(78,242,210,0.5); border-radius: 50%;
    box-shadow: 0 0 10px rgba(78,242,210,0.3), 0 0 20px rgba(78,242,210,0.12);
    display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
}
.bubble-assistant {
    display: inline-block; background-color: #4ef2d2;
    color: #0d1117 !important; -webkit-text-fill-color: #0d1117 !important;
    border-radius: 2px 16px 16px 16px; padding: 11px 16px;
    font-size: 0.95rem; font-weight: 500; line-height: 1.6; max-width: 72%;
    box-shadow: 0 2px 12px rgba(78,242,210,0.2);
}
.bubble-assistant * { color: #0d1117 !important; -webkit-text-fill-color: #0d1117 !important; }
.bubble-user {
    display: inline-block; background-color: #273344;
    color: #ffffff !important; -webkit-text-fill-color: #ffffff !important;
    border-radius: 16px 2px 16px 16px; padding: 11px 16px;
    font-size: 0.95rem; line-height: 1.6; max-width: 65%;
    box-shadow: 0 2px 10px rgba(0,0,0,0.25);
}
.bubble-user * { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
.bubble-welcome {
    color: #d1dce8 !important; -webkit-text-fill-color: #d1dce8 !important;
    font-size: 0.97rem; line-height: 1.6; padding: 8px 0 0 0;
}
.bubble-welcome strong { color: #4ef2d2 !important; -webkit-text-fill-color: #4ef2d2 !important; }

/* ── Chat input ── */
div[data-testid="stBottom"], div[data-testid="stChatInputContainer"],
div[data-testid="stChatInputContainer"] > div,
div[data-testid="stChatInputContainer"] > div > div {
    background-color: #141920 !important;
}
div[data-testid="stChatInput"] {
    background-color: #141920 !important; border: 1.5px solid #4ef2d2 !important;
    border-radius: 30px !important;
    box-shadow: 0 0 8px rgba(78,242,210,0.4), 0 0 20px rgba(78,242,210,0.2), 0 0 40px rgba(78,242,210,0.08) !important;
    padding: 4px 14px !important;
}
div[data-testid="stChatInput"] textarea {
    color: #d1dce8 !important; background: transparent !important;
    -webkit-text-fill-color: #d1dce8 !important;
}
div[data-testid="stChatInput"] textarea::placeholder { color: #4a5b6f !important; }
div[data-testid="stChatInput"] button {
    background-color: #4ef2d2 !important; border-radius: 50% !important;
    color: #0d1117 !important; box-shadow: 0 0 8px rgba(78,242,210,0.5) !important;
}

/* ── Cartes offres ── */
.job-card {
    background-color: #1a2535; border: 1px solid rgba(78,242,210,0.2);
    border-radius: 12px; padding: 16px 20px; margin-bottom: 14px;
}
.job-card:hover { border-color: rgba(78,242,210,0.5); }
.job-title { font-size: 1rem; font-weight: 700; color: #4ef2d2 !important; -webkit-text-fill-color: #4ef2d2 !important; }
.job-meta  { font-size: 0.82rem; color: #64748b !important; -webkit-text-fill-color: #64748b !important; margin: 4px 0 8px 0; }
.job-snippet { font-size: 0.88rem; color: #94a3b8 !important; -webkit-text-fill-color: #94a3b8 !important; line-height: 1.5; }
.job-link { font-size: 0.82rem; color: #4ef2d2 !important; -webkit-text-fill-color: #4ef2d2 !important; }
.score-badge {
    display: inline-block; padding: 4px 12px; border-radius: 20px;
    font-weight: 700; font-size: 0.9rem; margin: 8px 0;
}
.score-high { background-color: #0d3b2e; color: #4ef2d2 !important; -webkit-text-fill-color: #4ef2d2 !important; border: 1px solid #4ef2d2; }
.score-mid  { background-color: #2d2a10; color: #f0c040 !important; -webkit-text-fill-color: #f0c040 !important; border: 1px solid #f0c040; }
.score-low  { background-color: #2d1010; color: #e05a5a !important; -webkit-text-fill-color: #e05a5a !important; border: 1px solid #e05a5a; }
.analysis-box {
    background-color: #111820; border: 1px solid #2a3a50;
    border-radius: 10px; padding: 14px 18px; margin-top: 10px;
    font-size: 0.9rem; color: #d1dce8 !important; -webkit-text-fill-color: #d1dce8 !important; line-height: 1.7;
}
.analysis-box * { color: #d1dce8 !important; -webkit-text-fill-color: #d1dce8 !important; }

/* ── Fix : chat input fixé en bas de page ── */
div[data-testid="stBottom"] {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    width: 100% !important;
    background-color: #141920 !important;
    border-top: none !important;
    box-shadow: none !important;
    padding: 10px 0 16px 0 !important;
    z-index: 9999 !important;
    display: block !important;
}
div[data-testid="stBottom"] > div,
div[data-testid="stBottom"] > div > div {
    max-width: 920px !important;
    margin: 0 auto !important;
    padding: 0 1rem !important;
    background-color: #141920 !important;
}
/* Espace en bas pour que les messages ne se cachent pas derrière la barre */
.block-container {
    padding-bottom: 120px !important;
}

/* ── Titres et sous-titres en blanc dans l'onglet Recherche ── */
.block-container h1, .block-container h2, .block-container h3,
.block-container h4, .block-container h5, .block-container h6 {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
/* Titres écrits via st.markdown("### ...") */
.block-container div.stMarkdown h1,
.block-container div.stMarkdown h2,
.block-container div.stMarkdown h3,
.block-container div.stMarkdown h4 {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* ── Misc ── */
hr { border-color: #1e2a38 !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #2a3a50; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #4ef2d2; }
</style>
"""
