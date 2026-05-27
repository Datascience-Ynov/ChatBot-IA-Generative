"""
Services métier : LLM, parsing CV, recherche d'offres, analyse de compatibilité.
"""

from __future__ import annotations
import json
import re
from typing import Generator

import pdfplumber
import jobspy
from openai import OpenAI

from .models import Message, JobOffer


class LLMService:
    """Wraps le client NVIDIA NIM (OpenAI-compatible)."""

    def __init__(self, api_key: str) -> None:
        self._client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key,
        )

    def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.5,
        max_tokens: int = 1024,
    ) -> Generator[str, None, None]:
        """Génère les tokens un par un (streaming)."""
        payload = [{"role": m.role, "content": m.content} for m in messages]
        response = self._client.chat.completions.create(
            model=model,
            messages=payload,
            temperature=temperature,
            top_p=0.7,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def complete(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> str:
        """Retourne la réponse complète (non-streaming)."""
        return "".join(self.stream(messages, model, temperature, max_tokens))


class CVParser:
    """Extrait le texte brut d'un fichier PDF uploadé."""

    @staticmethod
    def extract(uploaded_file) -> str:
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join(
                page.extract_text() or "" for page in pdf.pages
            ).strip()


class JobSearchService:
    """Recherche des offres d'emploi via JobSpy (LinkedIn + Indeed + Glassdoor).
    Gratuit, sans clé API, sans inscription.
    """

    def __init__(self, max_results: int = 6) -> None:
        self._max = max_results

    def search(self, query: str, location: str = "France") -> list[JobOffer]:
        # Sépare le titre du reste si l'utilisateur a mis une location dans la query
        df = jobspy.scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor"],
            search_term=query,
            location=location,
            results_wanted=self._max,
            hours_old=72,           # offres des 3 derniers jours
            country_indeed="France",
        )

        results: list[JobOffer] = []
        for _, row in df.iterrows():
            desc = str(row.get("description") or "")
            results.append(JobOffer(
                title=str(row.get("title", "Sans titre")),
                url=str(row.get("job_url", "#")),
                body=desc[:800],   # on tronque pour ne pas surcharger le LLM
                source=str(row.get("company", "")),
            ))
        return results


class CompatibilityAnalyzer:
    """Analyse la compatibilité entre un CV et une offre d'emploi via LLM."""

    _PROMPT = """Tu es un expert en recrutement tech.
Voici un CV :
--- CV ---
{cv}

Voici une offre d'emploi :
--- OFFRE ---
{job}

Réponds UNIQUEMENT avec ce format JSON (rien d'autre) :
{{
  "score": <entier 0-100>,
  "points_forts": "<2-3 points forts du candidat pour ce poste>",
  "points_faibles": "<1-2 écarts ou manques>",
  "conseil": "<une action concrète pour améliorer la candidature>"
}}"""

    def __init__(self, llm: LLMService, model: str) -> None:
        self._llm   = llm
        self._model = model

    def analyze(self, cv_text: str, offer: JobOffer) -> JobOffer:
        prompt = self._PROMPT.format(cv=cv_text[:3000], job=offer.body[:1500])
        raw = self._llm.complete(
            [Message("user", prompt)],
            model=self._model,
            temperature=0.2,
            max_tokens=512,
        )
        try:
            data = json.loads(re.search(r"\{.*\}", raw, re.DOTALL).group())
            offer.score    = int(data.get("score", 0))
            offer.analysis = (
                f"**Points forts :** {data.get('points_forts', '')}\n\n"
                f"**Points faibles :** {data.get('points_faibles', '')}\n\n"
                f"**Conseil :** {data.get('conseil', '')}"
            )
        except Exception:
            offer.score    = 0
            offer.analysis = raw
        return offer
