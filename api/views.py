
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from .models import User, Kategori, Promo, Produk, Pembayaran, Trans_h, Trans_d
from .serializers import *

from .serializers import UserSerializer

# Custom serializer JWT
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # validasi bawaan
        user = self.user  # ambil user yang berhasil login

        if not user.is_active:
            raise serializers.ValidationError("Akun tidak aktif.")

        # Ambil role yang diminta dari frontend
        requested_role = self.context['request'].data.get('role')
        if requested_role and user.role != requested_role:
            raise serializers.ValidationError("Role tidak sesuai.")

        # Tambahkan role & username ke response token
        data['role'] = user.role
        data['username'] = user.username
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

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

class KategoriListCreate(generics.ListCreateAPIView):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer
    permission_classes = [IsAuthenticated]  # wajib login

class PromoListCreate(generics.ListCreateAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

class PembayaranListCreate(generics.ListCreateAPIView):
    queryset = Pembayaran.objects.all()
    serializer_class = PembayaranSerializer

class TransHListCreate(generics.ListCreateAPIView):
    queryset = Trans_h.objects.all()
    serializer_class = TransHSerializer

class TransDListCreate(generics.ListCreateAPIView):
    queryset = Trans_d.objects.all()
    serializer_class = TransDSerializer

class ProdukViewSet(viewsets.ModelViewSet):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer
    permission_classes = [AllowAny]

class DataView(APIView):
    def get(self, request):
        return Response({"pesan": "Halo dari backend Django!"})