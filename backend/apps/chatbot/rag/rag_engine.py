import faiss
import pickle
from sentence_transformers import SentenceTransformer
from pathlib import Path

from apps.chatbot.llm.groq_client import GroqLLM

# Base du projet
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# FAISS_DIR pointe vers le dossier data/faiss_index au même niveau que backend
FAISS_DIR = BASE_DIR.parent / "data" / "faiss_index"


class RAGEngine:
    def __init__(self):
        # Vérifier que les fichiers FAISS existent
        index_path = FAISS_DIR / "index.faiss"
        meta_path = FAISS_DIR / "meta.pkl"

        if not index_path.exists() or not meta_path.exists():
            raise FileNotFoundError(
                f"Fichiers FAISS manquants. Vérifiez que {index_path} et {meta_path} existent."
            )

        # Charger FAISS
        self.index = faiss.read_index(str(index_path))

        # Charger documents
        with open(meta_path, "rb") as f:
            self.documents = pickle.load(f)

        # Embeddings
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        # LLM utilisé uniquement pour reformuler à partir du contexte FAISS
        self.llm = GroqLLM(
            faiss_index_path=str(index_path),
            meta_path=str(meta_path),
        )

    def retrieve(self, question, top_k=3):
        """Récupère les documents les plus proches pour une question donnée."""
        q_emb = self.embedder.encode([question])
        distances, indices = self.index.search(q_emb, top_k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.documents):
                results.append(self.documents[idx])

        return results

    def query(self, question, top_k=3):
        """
        Retourne une réponse basée sur les documents FAISS.
        Le LLM est utilisé uniquement pour reformuler les réponses extraites,
        sans jamais inventer d'informations.
        """
        docs = self.retrieve(question, top_k)

        if not docs:
            return [{
                "answer": (
                    "Je ne dispose pas d’informations officielles sur cette question. "
                    "Veuillez poser une question liée à CitizenLab Sénégal."
                ),
                "source": "CitizenLab Sénégal",
                "confidence": "low"
            }]

        # Construire le contexte strict pour le LLM
        context = "Réponds uniquement avec les informations suivantes :\n\n"
        for d in docs:
            context += f"- {d['question']} : {d['answer']}\n"

        # Appel LLM (sans prompt supplémentaire)
        final_answer = self.llm.generate(
            question=question,
            context=context,
            top_k=top_k
        )

        return [{
            "answer": final_answer,
            "source": "Base documentaire CitizenLab Sénégal",
            "confidence": "institutionnelle"
        }]
