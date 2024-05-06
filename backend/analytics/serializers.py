from rest_framework import serializers


class DictionaryContentSerializer(serializers.Serializer):
    dictionary_name = serializers.CharField(max_length=255)
    content = serializers.DictField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
