from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    ProfileSerializer,
)
from .models import CustomUser, Profile


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        Profile.objects.create(user=user)
        refresh = RefreshToken.for_user(user)
        token = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(token, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
