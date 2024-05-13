from rest_framework import serializers
from .models import Friendship
from django.contrib.auth import get_user_model


class FriendshipSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    friend = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Friendship
        fields = ["user", "friend", "created_at"]
        read_only_fields = ["created_at"]

    def validate(self, data):
        user = data["user"]
        friend = data["friend"]

        if user == friend:
            raise serializers.ValidationError("Cannot add yourself as a friend.")

        if Friendship.objects.filter(user=user, friend=friend).exists():
            raise serializers.ValidationError("Friendship already exists.")

        return data
