import os
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

DATA_PATH = "rag_pipeline/data/cleaned"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

documents = []

for file in os.listdir(DATA_PATH):
    if file.endswith(".csv"):
        df = pd.read_csv(
            os.path.join(DATA_PATH, file),
            sep=None,
            engine="python",
            encoding="utf-8",
            on_bad_lines="skip"
        )

        full_text = []
        for _, row in df.iterrows():
            row_text = " | ".join(
                [f"{col}: {row[col]}" for col in df.columns if pd.notna(row[col])]
            )
            if row_text.strip():
                full_text.append(row_text)

        documents.append(
            Document(
                page_content="\n".join(full_text),
                metadata={"source": file}
            )
        )

# Découpage
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# FAISS
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("faiss_index")

print("Index FAISS CitizenLab créé.")
