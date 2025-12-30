import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

# 4 niveaux au-dessus de rag_engine.py pour atteindre la racine du projet
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
DATA_DIR = os.path.join(BASE_DIR, "data", "faiss_index")

class RAGEngine:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        index_path = os.path.join(DATA_DIR, "index.faiss")
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index FAISS non trouvé : {index_path}")
        self.index = faiss.read_index(index_path)

        meta_path = os.path.join(DATA_DIR, "meta.pkl")
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Fichier meta.pkl non trouvé : {meta_path}")
        with open(meta_path, "rb") as f:
            self.documents = pickle.load(f)

    def query(self, question, top_k=3):
        embedding = self.model.encode([question])
        distances, indices = self.index.search(embedding, top_k)

        answers = []
        for idx in indices[0]:
            doc = self.documents[idx]
            if isinstance(doc, dict) and "answer" in doc:
                answers.append(doc["answer"])
            else:
                answers.append(str(doc))
        return answers
