from rest_framework import viewsets

from authx.utils import NoPagination
from .models import Friendship
from .serializers import FriendshipSerializer


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    pagination = NoPagination
