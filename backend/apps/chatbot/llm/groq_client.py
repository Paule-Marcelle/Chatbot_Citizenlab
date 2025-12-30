import os
import pickle
import faiss
from groq import Groq
from sentence_transformers import SentenceTransformer

class GroqLLM:
    def __init__(self, model="openai/gpt-oss-120b", faiss_index_path=None, meta_path=None):
        if faiss_index_path is None or meta_path is None:
            raise ValueError("Veuillez fournir faiss_index_path et meta_path valides")

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY non définie")

        self.client = Groq(api_key=api_key)
        self.model = model

        # Charger FAISS
        self.index = faiss.read_index(faiss_index_path)

        # Charger les documents (meta.pkl doit contenir une liste des textes)
        with open(meta_path, "rb") as f:
            self.documents = pickle.load(f)

    def retrieve_top_docs(self, query, top_k=3):
        model = SentenceTransformer("all-MiniLM-L6-v2")
        q_emb = model.encode([query])
        D, I = self.index.search(q_emb, top_k)
        
        top_docs = []
        for i in I[0]:
            doc = self.documents[i]
            # Concaténer question + answer
            text = f"{doc['question']} {doc['answer']}"
            top_docs.append(text)
        
        return top_docs
    def generate(self, question: str, context: str = None, top_k=3) -> str:
        # Si context non fourni, récupérer top_k documents depuis FAISS
        if context is None:
            top_docs = self.retrieve_top_docs(question, top_k=top_k)
            context = "\n\n".join(top_docs)

        prompt = f"""
Tu es le chatbot institutionnel officiel de CitizenLab Sénégal.
Réponds de manière claire, professionnelle et crédible.

CONTEXTE OFFICIEL :
{context}

QUESTION :
{question}

RÉPONSE :
"""

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Assistant institutionnel CitizenLab Sénégal"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_completion_tokens=512,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
            stop=None
        )

        return completion.choices[0].message.content.strip()
