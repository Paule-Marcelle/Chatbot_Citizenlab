"""
VERSION SÉCURISÉE du Chatbot RAG avec variables d'environnement
REMPLACE chatbot_rag.py avec gestion sécurisée des clés API
"""

import os
from pathlib import Path
from typing import List, Dict
import numpy as np
import pandas as pd
from groq import Groq
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

class ChatbotRAG:
    def __init__(self, groq_api_key: str = None, csv_folder: str = "knowledge_base"):
        """
        Initialise le chatbot avec Groq et charge la base de connaissances
        
        Args:
            groq_api_key: Clé API Groq (si None, charge depuis .env)
            csv_folder: Dossier contenant vos fichiers CSV
        """
        # ✅ SÉCURISÉ : Charge la clé depuis .env si non fournie
        if groq_api_key is None:
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError(
                    "❌ Clé API Groq manquante!\n"
                    "   Créez un fichier .env avec: GROQ_API_KEY=votre_clé_ici\n"
                    "   OU passez la clé en paramètre: ChatbotRAG(groq_api_key='...')"
                )
        
        # Configuration Groq
        self.client = Groq(api_key=groq_api_key)
        self.model = "llama-3.3-70b-versatile"
        
        # Modèle d'embeddings multilingue
        print("📥 Chargement du modèle d'embeddings...")
        self.embedder = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        
        # Stockage des données
        self.documents = []
        self.embeddings = None
        self.index = None
        self.csv_folder = csv_folder
        
        # Historique de conversation
        self.conversation_history = []
        
        print("✅ Chatbot initialisé avec succès!")
    
    def load_csv_files(self):
        """Charge tous les fichiers CSV de la base de connaissances"""
        
        csv_files = list(Path(self.csv_folder).glob("*.csv"))
        
        if not csv_files:
            raise FileNotFoundError(f"Aucun fichier CSV trouvé dans {self.csv_folder}")
        
        print(f"📄 {len(csv_files)} fichier(s) CSV trouvé(s)")
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                print(f"   ✓ {csv_file.name}: {len(df)} lignes")
                
                for _, row in df.iterrows():
                    text_parts = []
                    metadata = {"source": csv_file.name}
                    
                    for col in df.columns:
                        if pd.notna(row[col]):
                            value = str(row[col])
                            text_parts.append(f"{col}: {value}")
                            metadata[col] = value
                    
                    doc = {
                        "text": " | ".join(text_parts),
                        "metadata": metadata
                    }
                    self.documents.append(doc)
            
            except Exception as e:
                print(f"   ✗ Erreur avec {csv_file.name}: {e}")
        
        print(f"\n✅ Total: {len(self.documents)} documents chargés")
    
    def create_vector_index(self, save_path: str = "vector_index"):
        """Crée l'index vectoriel FAISS"""
        print("\n🔧 Création de l'index vectoriel...")
        
        texts = [doc["text"] for doc in self.documents]
        print(f"   📊 Génération des embeddings pour {len(texts)} documents...")
        self.embeddings = self.embedder.encode(texts, show_progress_bar=True)
        
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype('float32'))
        
        os.makedirs(save_path, exist_ok=True)
        faiss.write_index(self.index, f"{save_path}/faiss.index")
        
        with open(f"{save_path}/documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)
        
        print(f"✅ Index vectoriel créé et sauvegardé dans '{save_path}'")
    
    def load_vector_index(self, save_path: str = "vector_index"):
        """Charge un index vectoriel existant"""
        try:
            self.index = faiss.read_index(f"{save_path}/faiss.index")
            with open(f"{save_path}/documents.pkl", "rb") as f:
                self.documents = pickle.load(f)
            print(f"✅ Index vectoriel chargé depuis '{save_path}'")
            return True
        except:
            print(f"⚠️  Aucun index trouvé dans '{save_path}'")
            return False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Recherche les documents les plus pertinents"""
        query_embedding = self.embedder.encode([query])
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc["score"] = float(distance)
                results.append(doc)
        
        return results
    
    def generate_response(self, user_message: str, context_docs: List[Dict]) -> str:
        """Génère une réponse avec Groq"""
        context_text = "\n\n".join([
            f"Document {i+1}:\n{doc['text']}" 
            for i, doc in enumerate(context_docs)
        ])
        
        system_prompt = f"""Tu es un assistant conversationnel expert sur CitizenLab Sénégal et la participation citoyenne au Senegal.

CONTEXTE PERTINENT:
{context_text}

INSTRUCTIONS:
- Réponds en français de manière naturelle et conversationnelle
- Base-toi PRIORITAIREMENT sur le contexte fourni ci-dessus
- Si l'information n'est pas dans le contexte, dis-le honnêtement
- Sois précis avec les chiffres et les faits
- Utilise un ton amical et accessible
- Si on te demande des informations de contact ou des liens, indique que tu n'as pas ces informations spécifiques mais tu peux orienter l'utilisateur"""

        messages = [{"role": "system", "content": system_prompt}]
        
        for msg in self.conversation_history[-10:]:
            messages.append(msg)
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=0.9
            )
            
            assistant_message = response.choices[0].message.content
            
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
        
        except Exception as e:
            return f"❌ Erreur lors de la génération de la réponse: {e}"
    
    def chat(self, user_message: str, top_k: int = 5, show_sources: bool = True) -> str:
        """Interface principale du chatbot"""
        relevant_docs = self.search(user_message, top_k=top_k)
        response = self.generate_response(user_message, relevant_docs)
        
        if show_sources and relevant_docs:
            sources = "\n\n📚 Sources utilisées:"
            for i, doc in enumerate(relevant_docs[:3], 1):
                source = doc['metadata'].get('source', 'Inconnu')
                sources += f"\n   {i}. {source}"
            response += sources
        
        return response
    
    def reset_conversation(self):
        """Réinitialise l'historique de conversation"""
        self.conversation_history = []
        print("🔄 Conversation réinitialisée")


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🤖 CHATBOT RAG CITIZENLAB SÉNÉGAL")
    print("=" * 60)
    
    # ✅ Charger depuis .env automatiquement
    try:
        chatbot = ChatbotRAG(csv_folder="knowledge_base")
    except ValueError as e:
        print(f"\n{e}")
        print("\n💡 CONSEIL: Créez un fichier .env avec votre clé API")
        return
    
    # Charger ou créer l'index
    if not chatbot.load_vector_index():
        chatbot.load_csv_files()
        chatbot.create_vector_index()
    
    # Boucle de conversation
    print("\n" + "=" * 60)
    print("💬 Conversation démarrée! (tapez 'quit' pour quitter, 'reset' pour réinitialiser)")
    print("=" * 60 + "\n")
    
    while True:
        user_input = input("Vous: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Au revoir!")
            break
        
        if user_input.lower() == 'reset':
            chatbot.reset_conversation()
            continue
        
        print("\n🤖 Assistant: ", end="")
        response = chatbot.chat(user_input, show_sources=True)
        print(response)
        print("\n" + "-" * 60 + "\n")


if __name__ == "__main__":
    main()