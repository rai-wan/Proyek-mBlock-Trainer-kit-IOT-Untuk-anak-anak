from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Ikan
from .serializers import UserSerializer, IkanSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# Register akun
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# Login JWT
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


# Ambil profil user
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        })


# Data dummy
class DataView(APIView):
    def get(self, request):
        return Response({"pesan": "Halo dari backend Django!"})


# CRUD Ikan — ✅ tanpa login
class IkanViewSet(viewsets.ModelViewSet):
    queryset = Ikan.objects.all()
    serializer_class = IkanSerializer
    permission_classes = [AllowAny]  # ✅ Akses publik tanpa token
