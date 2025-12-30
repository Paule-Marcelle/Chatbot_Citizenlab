import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

df = pd.read_csv("data/cleaned.csv")

texts = (df["question"] + " " + df["answer"]).tolist()

model = SentenceTransformer(MODEL_NAME)
embeddings = model.encode(texts, show_progress_bar=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "data/faiss_index/index.faiss")

with open("data/faiss_index/meta.pkl", "wb") as f:
    pickle.dump(df.to_dict(orient="records"), f)

print("✅ Index FAISS créé")
