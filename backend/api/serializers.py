from rest_framework import serializers

class TextEmbeddingSerializer(serializers.Serializer):
    text = serializers.CharField()
