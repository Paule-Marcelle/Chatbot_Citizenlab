"""
API REST pour le Chatbot CitizenLab
Framework: FastAPI
Usage: Intégration sur site web existant
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from chatbot_rag import ChatbotRAG
import uvicorn

# Charger les variables d'environnement
load_dotenv()

# Initialiser FastAPI
app = FastAPI(
    title="CitizenLab Chatbot API",
    description="API REST pour le chatbot conversationnel CitizenLab",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis votre site web
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React local
        "http://localhost:8000",  # Développement local
        "https://votre-site-web.com",  # REMPLACEZ par votre domaine
        "https://www.votre-site-web.com",
        "*"  # ATTENTION: À restreindre en production !
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO: Migrer vers Redis/Database pour production
chat_sessions = {}

# Initialiser le chatbot au démarrage
chatbot = None

@app.on_event("startup")
async def startup_event():
    """Initialise le chatbot au démarrage de l'API"""
    global chatbot
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY manquante dans .env")
    
    print("🚀 Initialisation du chatbot...")
    chatbot = ChatbotRAG(groq_api_key=groq_api_key, csv_folder="knowledge_base")
    
    if not chatbot.load_vector_index():
        print("📚 Création de l'index vectoriel...")
        chatbot.load_all_files()  # Charge CSV + TXT
        chatbot.create_vector_index()
    
    print("✅ Chatbot prêt!")

# Modèles de données (Pydantic)
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    top_k: Optional[int] = 5
    show_sources: Optional[bool] = True

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: Optional[List[str]] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    documents_loaded: int

# Routes de l'API

@app.get("/", tags=["Info"])
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "CitizenLab Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Info"])
async def health_check():
    """Vérifier l'état de santé de l'API"""
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot non initialisé")
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "documents_loaded": len(chatbot.documents)
    }

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(message: ChatMessage):
    """
    Endpoint principal pour envoyer un message au chatbot
    
    Args:
        message: Message de l'utilisateur avec paramètres optionnels
    
    Returns:
        Réponse du chatbot avec sources
    
    Example:
        POST /chat
        {
            "message": "Quels sont les objectifs de CitizenLab ?",
            "session_id": "user123",
            "top_k": 5,
            "show_sources": false 
        }
    """
    if chatbot is None:
        raise HTTPException(status_code=503, detail="Chatbot non disponible")
    
    try:
        # Créer une session si elle n'existe pas
        if message.session_id not in chat_sessions:
            chat_sessions[message.session_id] = ChatbotRAG(
                groq_api_key=os.getenv("GROQ_API_KEY"),
                csv_folder="knowledge_base"
            )
            chat_sessions[message.session_id].documents = chatbot.documents
            chat_sessions[message.session_id].embeddings = chatbot.embeddings
            chat_sessions[message.session_id].index = chatbot.index
            chat_sessions[message.session_id].embedder = chatbot.embedder
        
        # Obtenir la réponse
        session_chatbot = chat_sessions[message.session_id]
        response = session_chatbot.chat(
            message.message,
            top_k=message.top_k,
            show_sources=message.show_sources
        )
        
        # Extraire les sources si demandées
        sources = None
        if message.show_sources and "📚 Sources utilisées:" in response:
            response_parts = response.split("📚 Sources utilisées:")
            response = response_parts[0].strip()
            sources = [s.strip() for s in response_parts[1].strip().split("\n") if s.strip()]
        
        return {
            "response": response,
            "session_id": message.session_id,
            "sources": sources
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.post("/chat/reset/{session_id}", tags=["Chat"])
async def reset_conversation(session_id: str):
    """
    Réinitialiser une conversation
    
    Args:
        session_id: ID de la session à réinitialiser
    """
    if session_id in chat_sessions:
        chat_sessions[session_id].reset_conversation()
        return {"message": f"Session {session_id} réinitialisée"}
    else:
        raise HTTPException(status_code=404, detail="Session non trouvée")

@app.delete("/chat/session/{session_id}", tags=["Chat"])
async def delete_session(session_id: str):
    """
    Supprimer une session de chat
    
    Args:
        session_id: ID de la session à supprimer
    """
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return {"message": f"Session {session_id} supprimée"}
    else:
        raise HTTPException(status_code=404, detail="Session non trouvée")

@app.get("/stats", tags=["Info"])
async def get_stats():
    """Obtenir des statistiques sur l'utilisation de l'API"""
    return {
        "active_sessions": len(chat_sessions),
        "total_documents": len(chatbot.documents) if chatbot else 0,
        "model": chatbot.model if chatbot else "N/A"
    }

# Route pour tester l'API facilement
@app.get("/test", tags=["Test"])
async def test_chat():
    """Endpoint de test simple"""
    test_message = ChatMessage(
        message="Qu'est-ce que CitizenLab Sénégal ?",
        session_id="test",
        top_k=3,
        show_sources=True
    )
    return await chat(test_message)

if __name__ == "__main__":
    # Lancer le serveur
    uvicorn.run(
        "api_chatbot:app",
        host="0.0.0.0",  # Accessible depuis l'extérieur
        port=8000,
        reload=True  # Auto-reload en développement
    )