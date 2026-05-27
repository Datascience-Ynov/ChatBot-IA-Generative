"""
Chatbot IA Générative — Point d'entrée Streamlit
Auteur : Mourad Amoussa | Lyon Ynov M2 — Projet IA Générative
"""

from __future__ import annotations
import os

import streamlit as st
from dotenv import load_dotenv

from core import CSS, UI, Message
from core import LLMService, CVParser, JobSearchService, CompatibilityAnalyzer

load_dotenv()

MODELS = [
    "meta/llama-3.1-70b-instruct",
    "meta/llama-3.1-8b-instruct",
    "mistralai/mistral-7b-instruct-v0.3",
    "microsoft/phi-3-mini-128k-instruct",
]

DEFAULT_SYSTEM_PROMPT = (
    "Tu es un assistant IA intelligent, utile et bienveillant. "
    "Réponds toujours en français de manière claire et structurée. "
    "Si tu ne sais pas quelque chose, dis-le franchement."
)


class App:
    """Orchestre l'application Streamlit."""

    def __init__(self) -> None:
        st.set_page_config(page_title="Chatbot IA Générative", page_icon="🤖", layout="wide")
        st.markdown(CSS, unsafe_allow_html=True)

        api_key = os.getenv("NVIDIA_API_KEY", "")
        if not api_key:
            st.error("❌ Clé API NVIDIA manquante. Ajoute dans `.env` :\n```\nNVIDIA_API_KEY=nvapi-xxxx\n```")
            st.stop()

        self._llm        = LLMService(api_key)
        self._cv_parser  = CVParser()
        self._job_search = JobSearchService(max_results=6)

        self._init_state()
        self._render_sidebar()
        self._render_header()
        self._render_tabs()

    # ── Session state ──────────────────────────────────────────────────────
    def _init_state(self) -> None:
        for key, default in [("messages", []), ("cv_text", ""), ("job_offers", [])]:
            st.session_state.setdefault(key, default)

    # ── Sidebar ────────────────────────────────────────────────────────────
    def _render_sidebar(self) -> None:
        with st.sidebar:
            st.markdown('<span class="sidebar-title">⚙️ Configuration</span>', unsafe_allow_html=True)
            self.model = st.selectbox("Modèle", MODELS, index=0)
            self.system_prompt = st.text_area("System Prompt", value=DEFAULT_SYSTEM_PROMPT, height=130)
            st.markdown("<br>**Paramètres**", unsafe_allow_html=True)
            self.temperature = st.slider("Température", 0.0, 1.0, 0.5, 0.05)
            self.max_tokens  = st.slider("Tokens max",  256, 2048, 1024, 128)
            st.divider()
            if st.button("🗑️ Effacer la conversation", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("Propulsé par [NVIDIA NIM](https://build.nvidia.com) · Llama 3")

    # ── Header ─────────────────────────────────────────────────────────────
    def _render_header(self) -> None:
        model_short = self.model.split("/")[-1]
        st.markdown(f"""
        <div class="chat-header">
            <span class="robot-icon">🤖</span>
            <h1>Chatbot IA Générative</h1>
            <p class="caption">
                Modèle actif&nbsp;<code>{model_short}</code>
                &nbsp;&nbsp;Température&nbsp;<code>{self.temperature}</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

    # ── Tabs ───────────────────────────────────────────────────────────────
    def _render_tabs(self) -> None:
        # Le chat_input DOIT être déclaré hors des tabs pour se fixer en bas
        user_input = st.chat_input("Écrivez votre message ici...")

        tab_chat, tab_jobs = st.tabs(["💬  Chat", "🔍  Recherche d'offres & CV"])
        with tab_chat:
            self._tab_chat(user_input)
        with tab_jobs:
            self._tab_jobs()

    # ── Tab Chat ───────────────────────────────────────────────────────────
    def _tab_chat(self, user_input: str | None) -> None:
        if not st.session_state.messages:
            UI.render_welcome()

        for msg in st.session_state.messages:
            UI.render_message(msg["role"], msg["content"])

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            UI.render_message("user", user_input)
            self._stream_response()

    def _stream_response(self) -> None:
        messages = [Message("system", self.system_prompt)] + [
            Message(m["role"], m["content"]) for m in st.session_state.messages
        ]
        placeholder   = st.empty()
        full_response = ""
        try:
            for chunk in self._llm.stream(messages, self.model, self.temperature, self.max_tokens):
                full_response += chunk
                UI.render_streaming(placeholder, full_response, cursor=True)
            UI.render_streaming(placeholder, full_response, cursor=False)
        except Exception as e:
            full_response = f"❌ Erreur API : {e}"
            placeholder.error(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # ── Tab Offres ─────────────────────────────────────────────────────────
    def _tab_jobs(self) -> None:
        col_cv, col_search = st.columns([1, 1], gap="large")

        with col_cv:
            st.markdown("### 📄 Votre CV")
            uploaded = st.file_uploader("Uploader votre CV (PDF)", type=["pdf"])
            if uploaded:
                with st.spinner("Extraction du texte…"):
                    st.session_state.cv_text = self._cv_parser.extract(uploaded)
                st.success(f"✅ CV chargé — {len(st.session_state.cv_text)} caractères extraits")
                with st.expander("Aperçu du texte extrait"):
                    st.text(st.session_state.cv_text[:1200] + "…")
            elif st.session_state.cv_text:
                st.info("✅ CV déjà chargé en session.")

        with col_search:
            st.markdown("### 🔍 Recherche d'offres")
            query   = st.text_input("Intitulé / mots-clés", placeholder="ex: Data Scientist CDI Lyon")
            analyze = st.checkbox(
                "Analyser la compatibilité avec mon CV",
                disabled=not st.session_state.cv_text,
                help="Uploadez d'abord votre CV pour activer cette option",
            )
            search_btn = st.button("🔎 Rechercher", use_container_width=True)

        st.divider()

        if search_btn and query:
            with st.spinner("Recherche sur LinkedIn, Indeed, Glassdoor…"):
                try:
                    offers = self._job_search.search(query)
                except Exception as e:
                    st.error(f"⚠️ Erreur lors de la recherche : {e}")
                    return

            if not offers:
                st.warning("Aucune offre trouvée. Essaie d'autres mots-clés.")
                return

            if analyze and st.session_state.cv_text:
                analyzer = CompatibilityAnalyzer(self._llm, self.model)
                progress = st.progress(0, text="Analyse en cours…")
                for i, offer in enumerate(offers):
                    progress.progress((i + 1) / len(offers), text=f"Analyse {i+1}/{len(offers)}…")
                    offers[i] = analyzer.analyze(st.session_state.cv_text, offer)
                progress.empty()
                offers.sort(key=lambda o: o.score, reverse=True)

            st.session_state.job_offers = offers

        if st.session_state.job_offers:
            st.markdown(f"**{len(st.session_state.job_offers)} offre(s) trouvée(s)**")
            for offer in st.session_state.job_offers:
                UI.render_job_card(offer)


# ── Entry point ────────────────────────────────────────────────────────────────
App()
