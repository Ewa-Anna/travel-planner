from rest_framework import routers

from .viewsets import AccommodationViewSet, TransportationViewSet

app_name = "services"

router = routers.DefaultRouter()

router.register(r"accommodations", AccommodationViewSet)
router.register(r"transportations", TransportationViewSet)


urlpatterns = []

urlpatterns += router.urls
