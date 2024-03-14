from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from .models import TravelJournal, Photos, Review
from .serializers import TravelJournalSerializer, PhotosSerializer, ReviewSerializer


class TravelJournalViewSet(viewsets.ModelViewSet):
    queryset = TravelJournal.objects.all()
    serializer_class = TravelJournalSerializer
    parser_classes = [MultiPartParser, FormParser, FileUploadParser]


class PhotosViewSet(viewsets.ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotosSerializer
    parser_classes = [MultiPartParser, FormParser, FileUploadParser]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
