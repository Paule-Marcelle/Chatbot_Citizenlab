from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ChatRequestSerializer


class ChatbotAPIView(APIView):
    """
    API principale du chatbot CitizenLab
    """

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        question = serializer.validated_data["question"]

        # 🔹 TEMPORAIRE (mock)
        answer = (
            "Merci pour votre question. "
            "Le chatbot CitizenLab est actuellement en cours de déploiement."
        )

        return Response(
            {
                "question": question,
                "answer": answer,
                "confidence": "institutionnelle",
            },
            status=status.HTTP_200_OK
        )
