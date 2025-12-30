import faiss
import pickle
from sentence_transformers import SentenceTransformer
import os

os.makedirs("data/faiss_index", exist_ok=True)
index = faiss.read_index("data/faiss_index/index.faiss")

with open("data/faiss_index/meta.pkl", "rb") as f:
    documents = pickle.load(f)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def query_rag(question, top_k=3):
    q_emb = model.encode([question])
    distances, indices = index.search(q_emb, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(documents):
            # On récupère uniquement la réponse et on la met en phrase
            answer = documents[idx].get("answer", "")
            if answer:
                results.append(answer.strip())

    # Retourne une seule phrase cohérente (concatène les top_k réponses)
    return " ".join(results)


if __name__ == "__main__":
    res = query_rag(" Êtes-vous alignés avec les ODD ?")
    for r in res:
        print("Reponse :", res)
