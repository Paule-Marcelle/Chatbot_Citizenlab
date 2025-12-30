from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path
import os

from .serializers import ChatRequestSerializer
from ..llm.groq_client import GroqLLM

# 🔹 Définir les chemins vers FAISS et meta.pkl
BASE_DIR = Path(__file__).resolve().parents[3]  # remonte jusqu'à Chatbot_Citizenlab
FAISS_DIR = BASE_DIR / "data" / "faiss_index"

# 🔹 Initialiser le LLM avec FAISS et Meta
llm = GroqLLM(
    faiss_index_path=str(FAISS_DIR / "index.faiss"),
    meta_path=str(FAISS_DIR / "meta.pkl"),
    model="openai/gpt-oss-120b"
)


class ChatbotAPIView(APIView):
    """
    API principale du chatbot CitizenLab
    """

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        question = serializer.validated_data["question"]

        # 🔹 Récupérer la réponse via LLM + FAISS
        try:
            answer = llm.generate(question)
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la génération de réponse : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "question": question,
                "answer": answer,
                "source": "CitizenLab Sénégal – Base institutionnelle",
                "confidence": "institutionnelle",
            },
            status=status.HTTP_200_OK
        )
