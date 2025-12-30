from rest_framework import serializers

class ChatRequestSerializer(serializers.Serializer):
    question = serializers.CharField(
        required=True,
        max_length=1024,
        help_text="Question à poser au chatbot"
    )
