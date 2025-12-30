import sys
from pathlib import Path
import os

# Ajouter backend au sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configurer Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

# Chemins vers FAISS et meta
FAISS_DIR = BASE_DIR.parent / "data" / "faiss_index"
faiss_index_path = FAISS_DIR / "index.faiss"
meta_path = FAISS_DIR / "meta.pkl"

# Importer GroqLLM
from apps.chatbot.llm.groq_client import GroqLLM

# Créer l'instance avec les bons chemins
groq = GroqLLM(
    faiss_index_path=str(faiss_index_path),
    meta_path=str(meta_path),
    model="openai/gpt-oss-120b"
)

# Question
result = groq.generate(
    question="Qu’est-ce que CitizenLab Sénégal ?"
)

print("Réponse :", result)
