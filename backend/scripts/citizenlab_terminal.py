import sys
from pathlib import Path
import os

# backend/
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# Config Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

# Charger le RAG
from apps.chatbot.rag.rag_engine import RAGEngine

rag = RAGEngine()

print("\n🧠 CitizenLab – Assistant institutionnel")
print("Tape 'exit' pour quitter.\n")

while True:
    question = input("👤 Vous > ")

    if question.lower() in ["exit", "quit"]:
        print("\n👋 Fin de session.")
        break

    results = rag.query(question, top_k=3)

    if not results:
        print("\n🤖 CitizenLab > Je ne dispose pas d’informations officielles sur cette question.\n")
        continue

    print("\n🤖 CitizenLab >", results[0]["answer"], "\n")
