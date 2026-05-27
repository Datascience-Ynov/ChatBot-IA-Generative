# 🤖 Chatbot IA Générative

Projet réalisé dans le cadre du cours **Deep Learning — IA Générative**  
Mastère Data Scientist · Lyon Ynov Campus  
Auteur : **Mourad Amoussa**

🌐 **Application en ligne :** [https://chatbot-ia-generative-fu3iw9ev9ghgmbsnon9fc6.streamlit.app/](https://chatbot-ia-generative-fu3iw9ev9ghgmbsnon9fc6.streamlit.app/)

---

## 📌 Objectif

Développer une interface conversationnelle simple permettant d'interagir avec un **Large Language Model (LLM)** via une API d'IA générative.

---

## 🛠️ Technologies utilisées

| Technologie | Rôle |
|---|---|
| **Python 3.10+** | Langage principal |
| **Streamlit** | Framework d'interface web interactive |
| **NVIDIA NIM** | Plateforme d'accès aux LLMs (Llama 3, Mistral, Phi-3) |
| **OpenAI Python SDK** | Client API compatible NVIDIA NIM |
| **python-dotenv** | Gestion sécurisée de la clé API |

### Modèles disponibles
- `meta/llama-3.1-70b-instruct` ← modèle par défaut
- `meta/llama-3.1-8b-instruct`
- `mistralai/mistral-7b-instruct-v0.3`
- `microsoft/phi-3-mini-128k-instruct`

---

## ✨ Fonctionnalités

- 💬 **Interface de chat** avec historique de conversation persistant
- ⚡ **Streaming** des réponses token par token (effet "machine à écrire")
- 🎛️ **System prompt personnalisable** depuis la sidebar
- 🔄 **Choix du modèle** à la volée sans redémarrage
- 🌡️ **Paramètres de génération** ajustables (température, tokens max)
- 🗑️ **Effacement de l'historique** en un clic
- 🔐 **Gestion sécurisée** de la clé API via fichier `.env`
- 📄 **Upload de CV (PDF)** avec extraction automatique du texte
- 🔍 **Recherche d'offres d'emploi** en temps réel (LinkedIn, Indeed, Glassdoor)
- 🤝 **Analyse de compatibilité CV / offre** par le LLM avec score et conseils

---

## 🚀 Installation et lancement

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd chatbot_ia_generative
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la clé API

```bash
# Copier le fichier exemple
cp .env.example .env
```

Ouvrir `.env` et remplacer la valeur :
```
NVIDIA_API_KEY=nvapi-ta-vraie-clé-ici
```

> 🔑 Obtenir une clé gratuite : https://build.nvidia.com/explore/discover

### 5. Lancer l'application

```bash
streamlit run app.py
```

L'interface s'ouvre automatiquement sur http://localhost:8501

---

## 📁 Structure du projet

```
chatbot_ia_generative/
├── app.py                  # Application principale Streamlit
├── requirements.txt        # Dépendances Python
├── .env                    # Clé API (non versionné, à créer)
├── .env.example            # Template de configuration
├── README.md               # Ce fichier
├── .streamlit/
│   └── config.toml         # Thème sombre Streamlit
└── core/
    ├── __init__.py         # Exports du package
    ├── models.py           # Dataclasses (Message, JobOffer)
    ├── services.py         # LLMService, CVParser, JobSearchService, CompatibilityAnalyzer
    ├── ui.py               # Composants UI (bulles, cartes offres)
    └── styles.py           # CSS global injecté au démarrage
```

---

## 🏗️ Architecture technique

```
Utilisateur (navigateur)
        ↓ saisie texte
   Streamlit (app.py)
        ↓ messages formatés
   NVIDIA NIM API
   (integrate.api.nvidia.com)
        ↓ réponse streamée
   Streamlit (affichage progressif)
        ↓
   Historique session (st.session_state)
```

### Flux de données
1. L'utilisateur envoie un message
2. Streamlit construit la liste complète des messages (system prompt + historique + nouveau message)
3. Appel à l'API NVIDIA NIM avec `stream=True`
4. Les tokens arrivent un par un et s'affichent en temps réel
5. La réponse complète est sauvegardée dans `st.session_state.messages`

---

## 🌐 Démo en ligne

L'application est hébergée et accessible publiquement sur Streamlit Community Cloud :

👉 **[https://chatbot-ia-generative-fu3iw9ev9ghgmbsnon9fc6.streamlit.app/](https://chatbot-ia-generative-fu3iw9ev9ghgmbsnon9fc6.streamlit.app/)**

---

## 🔒 Sécurité

- La clé API est stockée dans un fichier `.env` **jamais versionné** (ajouté dans `.gitignore`)
- Ne jamais écrire la clé directement dans le code source

---

## 📚 Ressources

- [NVIDIA NIM — Documentation](https://docs.api.nvidia.com/)
- [Streamlit — Documentation](https://docs.streamlit.io/)
- [python-jobspy — Job scraping](https://github.com/Bunsly/JobSpy)
- [pdfplumber — PDF extraction](https://github.com/jsvine/pdfplumber)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
