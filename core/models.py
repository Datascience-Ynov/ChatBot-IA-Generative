"""
Domain models — structures de données partagées dans tout le projet.
"""

from dataclasses import dataclass, field


@dataclass
class Message:
    """Représente un message dans la conversation LLM."""
    role: str       # "user" | "assistant" | "system"
    content: str


@dataclass
class JobOffer:
    """Représente une offre d'emploi avec son analyse de compatibilité."""
    title:    str
    url:      str
    body:     str
    source:   str = ""
    analysis: str = ""
    score:    int = 0   # 0 – 100
