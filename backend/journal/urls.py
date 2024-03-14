from rest_framework import routers

from .viewsets import TravelJournalViewSet, PhotosViewSet, ReviewViewSet

app_name = "journal"

router = routers.DefaultRouter()
router.register(r"travel-journal", TravelJournalViewSet)
router.register(r"photos", PhotosViewSet)
router.register(r"reviews", ReviewViewSet)

urlpatterns = []

urlpatterns += router.urls
