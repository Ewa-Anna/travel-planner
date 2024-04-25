from django.db.models import Q
from django.contrib.auth import logout, get_user_model

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import get_user_from_token, NoPagination
from .serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
    PasswordResetConfirmSerializer,
    CustomUserSerializer,
    ProfileUpdateSerializer,
)
from .models import CustomUser, Profile


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        csrf_token = request.META.get("CSRF_COOKIE")
        response.data["csrf_token"] = csrf_token
        return response


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
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProfileUpdateSerializer
        return ProfileSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        profile_data = response.data
        return Response(
            {
                "success": True,
                "message": "Profile has been updated successfully",
                "result": profile_data,
            }
        )

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        profile_data = response.data
        return Response(
            {
                "success": True,
                "message": "Profile has been updated successfully",
                "result": profile_data,
            }
        )


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"success": True, "message": "Logout successful"}, status=status.HTTP_200_OK
        )


class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Your password has been changed."})

    def perform_update(self, serializer):
        serializer.save()


class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()

        return Response(
            {"message": "Account deactivated successfully."}, status=status.HTTP_200_OK
        )


class PasswordResetConfirmAPIView(APIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        password = serializer.validated_data["new_password"]

        user = get_user_from_token(token)

        if user is None:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password)
        user.save()

        return Response(
            {"success": "Password reset successfully"}, status=status.HTTP_200_OK
        )


class UserListView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    pagination_class = NoPagination

    def get_queryset(self):
        queryset = CustomUser.objects.all().order_by("first_name", "last_name")
        query_param = self.request.query_params.get("query")

        if query_param:
            queryset = queryset.filter(
                Q(first_name__icontains=query_param)
                | Q(last_name__icontains=query_param)
            )

        return queryset
