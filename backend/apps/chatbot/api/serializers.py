from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)


class ChatResponseSerializer(serializers.Serializer):
    answer = serializers.CharField()
    source = serializers.CharField(required=False)
