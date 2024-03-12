from rest_framework import routers

from .viewsets import CountryViewSet, CityViewSet, POIViewSet

app_name = "locations"

router = routers.DefaultRouter()
router.register(r"countries", CountryViewSet)
router.register(r"cities", CityViewSet)
router.register(r"pois", POIViewSet)

urlpatterns = []

urlpatterns += router.urls
