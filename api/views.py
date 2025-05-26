from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Kategori, Promo, Produk, Pembayaran, Trans_h, Trans_d
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView


# Register akun
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# Login JWT
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

# KATEGORI
class KategoriListCreate(generics.ListCreateAPIView):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer

# PROMO
class PromoListCreate(generics.ListCreateAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

# PEMBAYARAN
class PembayaranListCreate(generics.ListCreateAPIView):
    queryset = Pembayaran.objects.all()
    serializer_class = PembayaranSerializer

# TRANSAKSI HEADER
class TransHListCreate(generics.ListCreateAPIView):
    queryset = Trans_h.objects.all()
    serializer_class = TransHSerializer

# TRANSAKSI DETAIL
class TransDListCreate(generics.ListCreateAPIView):
    queryset = Trans_d.objects.all()
    serializer_class = TransDSerializer
    
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


# CRUD produk
class ProdukViewSet(viewsets.ModelViewSet):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer
    permission_classes = [AllowAny]  # ✅ Akses publik tanpa token
