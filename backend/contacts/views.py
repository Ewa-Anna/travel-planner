from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from authx.utils import NoPagination
from .models import Friendship
from .serializers import FriendshipSerializer


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    pagination = NoPagination
