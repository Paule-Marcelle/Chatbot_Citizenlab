# 🤖 Chatbot IA Open Source – CitizenLab Sénégal

## 📌 Présentation

Le **Chatbot IA CitizenLab Sénégal** est un assistant conversationnel intelligent conçu pour améliorer l’accès à l’information, renforcer la participation citoyenne et automatiser les réponses aux questions fréquentes sur CitizenLab Sénégal.

Le projet repose exclusivement sur des **technologies open source** et une **architecture RAG (Retrieval-Augmented Generation)** afin de garantir des réponses fiables, traçables, éthiques et institutionnelles.

---

## 🎯 Objectifs

### Objectif général
Fournir un chatbot fiable, inclusif et accessible pour informer, orienter et accompagner les citoyens, OSC, journalistes et partenaires institutionnels.

### Objectifs spécifiques
- Automatiser les FAQ institutionnelles
- Présenter CitizenLab Sénégal et AfricTivistes
- Orienter vers les formations, événements et appels à projets
- Réduire la charge humaine du support
- Collecter du feedback structuré
- Garantir la neutralité et la crédibilité des réponses

---

## 👥 Utilisateurs cibles

- Jeunes citoyens et étudiants  
- Organisations de la société civile (OSC)  
- Journalistes et médias  
- Partenaires institutionnels et bailleurs  
- Citoyens peu connectés ou débutants numériques  

---

## 🧠 Principe IA (RAG)

Le chatbot utilise une approche **Retrieval-Augmented Generation** :

1. L’utilisateur pose une question
2. Le système recherche des documents pertinents dans une base interne
3. Le LLM génère une réponse basée uniquement sur ces sources
4. En cas d’incertitude, le chatbot redirige vers un humain

Avantages :
- Pas d’hallucinations
- Réponses traçables
- Respect du cadre institutionnel

---

## 🏗️ Architecture Technique (Open Source)
Utilisateur → Widget Chat (React) → Backend API (FastAPI) → Orchestrateur IA (LangChain / LlamaIndex) → LLM Open Source → Base Vectorielle (ChromaDB / FAISS) → Base de connaissances (CSV, PDF, Docs)



---

## 🧩 Stack Technique

### Frontend
- React.js / Next.js
- Tailwind CSS
- Widget chat flottant
- i18n (FR / EN / Wolof – roadmap)

### Backend
- FastAPI (Python)
- JWT (sécurité)
- REST API
- CORS

### IA / NLP
- LLM Open Source :
  - Mistral 7B
  - LLaMA 3
  - Mixtral
  - Aya (multilingue)
- Déploiement via :
  - Ollama
  - vLLM
  - Hugging Face TGI

### RAG
- Embeddings :
  - sentence-transformers
  - multilingual-e5
  - bge-base-fr
- Vector DB :
  - ChromaDB (recommandé)
  - FAISS
  - Weaviate (OSS)

### Base de données
- PostgreSQL ou MongoDB
- Logs anonymisés
- Feedback utilisateurs
- Formulaires

---

## 📂 Sources de données

- CSV FAQ institutionnel
- Documents PDF
- Rapports et présentations
- Pages web validées

---

## 🔐 Sécurité & Éthique

- HTTPS obligatoire
- Aucune donnée sensible stockée
- Anonymisation automatique
- Consentement utilisateur
- Neutralité politique stricte
- IA explicable et auditée
- Le chatbot peut répondre : *« Je ne sais pas »*

---

## 🧠 Personnalité du chatbot

- Ton : professionnel, inclusif, poli
- Style : clair, pédagogique, concis
- Positionnement : institutionnel et neutre

---

## 📊 Indicateurs de performance (KPIs)

- Temps de réponse < 8 secondes
- ≥ 80 % de questions traitées automatiquement
- ≥ 70 % de satisfaction utilisateur
- Réduction des emails de support
- Disponibilité 24h/24

---

## 🚀 Déploiement

- Docker
- Docker Compose
- VPS ou serveur local
- Déploiement possible en souveraineté locale

---

## 🛣️ Roadmap

### Phase 1
- FAQ intelligente (CSV + PDF)
- RAG fonctionnel
- Interface web

### Phase 2
- Formulaires conversationnels
- Dashboard admin
- Feedback utilisateur

### Phase 3
- Multilingue (Wolof / Anglais)
- Voice bot (STT / TTS)
- Intégration réseaux sociaux

---

## 📦 Livrables

- Chatbot IA fonctionnel
- Backend API
- Base de connaissances structurée
- Dashboard d’administration
- Documentation technique
- Guide utilisateur

---

## 📜 Licence

Projet basé sur des technologies **open source**.  
Licence finale à définir selon la politique de CitizenLab Sénégal.

---

## ✨ Portage

Projet conçu pour **CitizenLab Sénégal**,  
dans une logique de **souveraineté numérique, inclusion et innovation civique**.
