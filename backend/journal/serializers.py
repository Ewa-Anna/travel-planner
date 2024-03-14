from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer

from .models import TravelJournal, Photos, Review


class TravelJournalSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = TravelJournal
        fields = "__all__"


class PhotosSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Photos
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
