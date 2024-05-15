from django.db.models import Q

from rest_framework import viewsets

from authx.utils import NoPagination

from .models import Friendship
from .serializers import FriendshipSerializer, FriendshipReadSerializer


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    pagination = NoPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Friendship.objects.filter(user=user).order_by(
            "friend__first_name", "friend__last_name"
        )
        query_param = self.request.query_params.get("query")

        if query_param:
            queryset = queryset.filter(
                Q(friend__first_name__icontains=query_param)
                | Q(friend__last_name__icontains=query_param)
            )

        return queryset

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return FriendshipReadSerializer
        return FriendshipSerializer
