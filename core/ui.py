"""
Composants UI — helpers de rendu HTML statiques pour Streamlit.
"""

from __future__ import annotations
import html as _html

import streamlit as st

from .models import JobOffer


class UI:
    """Méthodes statiques de rendu des éléments visuels."""

    # ── Bulles de chat ─────────────────────────────────────────────────────

    @staticmethod
    def render_message(role: str, content: str) -> None:
        """Affiche une bulle utilisateur ou assistant."""
        safe = _html.escape(content).replace("\n", "<br>")
        if role == "assistant":
            st.markdown(f"""
            <div class="msg-row assistant">
                <div class="avatar">🤖</div>
                <div class="bubble-assistant">{safe}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row user">
                <div class="avatar">👤</div>
                <div class="bubble-user">{safe}</div>
            </div>""", unsafe_allow_html=True)

    @staticmethod
    def render_streaming(placeholder, text: str, cursor: bool = True) -> None:
        """Met à jour le placeholder avec le texte streamé."""
        safe = _html.escape(text).replace("\n", "<br>")
        cur  = "▌" if cursor else ""
        placeholder.markdown(f"""
        <div class="msg-row assistant">
            <div class="avatar">🤖</div>
            <div class="bubble-assistant">{safe}{cur}</div>
        </div>""", unsafe_allow_html=True)

    @staticmethod
    def render_welcome() -> None:
        """Affiche le message d'accueil (conversation vide)."""
        st.markdown("""
        <div class="msg-row assistant">
            <div class="avatar">🤖</div>
            <div class="bubble-welcome">
                👋 Bonjour ! Je suis votre assistant IA propulsé par
                <strong>Llama 3</strong> via NVIDIA NIM.
                Posez-moi n'importe quelle question, je suis là pour vous aider !
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Cartes offres d'emploi ─────────────────────────────────────────────

    @staticmethod
    def render_job_card(offer: JobOffer) -> None:
        """Affiche une carte offre avec score et analyse si disponibles."""
        score_class = (
            "score-high" if offer.score >= 70
            else "score-mid" if offer.score >= 40
            else "score-low"
        )
        score_html = (
            f'<span class="score-badge {score_class}">Compatibilité : {offer.score} %</span>'
            if offer.score else ""
        )
        analysis_html = ""
        if offer.analysis:
            safe_analysis = (
                _html.escape(offer.analysis)
                .replace("\n", "<br>")
                .replace("**Points forts :**", "<strong>Points forts :</strong>")
                .replace("**Points faibles :**", "<strong>Points faibles :</strong>")
                .replace("**Conseil :**", "<strong>Conseil :</strong>")
            )
            analysis_html = f'<div class="analysis-box">{safe_analysis}</div>'

        st.markdown(f"""
        <div class="job-card">
            <div class="job-title">{_html.escape(offer.title)}</div>
            <div class="job-meta">🔗 {_html.escape(offer.source)}</div>
            <div class="job-snippet">{_html.escape(offer.body[:280])}…</div>
            {score_html}
            {analysis_html}
            <a class="job-link" href="{offer.url}" target="_blank">→ Voir l'offre complète</a>
        </div>
        """, unsafe_allow_html=True)
