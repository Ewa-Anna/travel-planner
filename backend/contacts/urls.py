from django.urls import path, include

from rest_framework import routers

from .views import FriendshipViewSet

app_name = "contacts"

router = routers.DefaultRouter()
router.register(r"friendships", FriendshipViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
