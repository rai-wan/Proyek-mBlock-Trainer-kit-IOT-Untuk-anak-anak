from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser

from .models import User, Kategori, Promo, Produk, Pembayaran, Trans_h, Trans_d
from .serializers import *
from .serializers import UserSerializer
from .models import TransaksiShop
from .serializers import TransaksiShopSerializer
from .models import StokMasuk
from .serializers import StokMasukSerializer

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
    permission_classes = [IsAuthenticated]  

class PromoListCreate(generics.ListCreateAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    permission_classes = [AllowAny] 

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Tambah stok jika dikirim
        jumlah_tambah = request.data.get('jumlah')
        if jumlah_tambah:
            try:
                jumlah_tambah = int(jumlah_tambah)
                instance.stok += jumlah_tambah
            except:
                return Response({"error": "Jumlah harus angka"}, status=400)

        # Update manual field yang dikirim (tanpa mengganggu yang tidak dikirim)
        instance.nama = request.data.get('nama', instance.nama)
        instance.deskripsi = request.data.get('deskripsi', instance.deskripsi)
        instance.harga = request.data.get('harga', instance.harga)

        # Update harga_satuan jika dikirim (dipakai suplayer)
        if 'harga_satuan' in request.data:
            instance.harga = request.data.get('harga_satuan')

        # Update kategori jika dikirim
        if 'kategori' in request.data:
            instance.kategori_id = request.data.get('kategori')

        # Update promo jika dikirim
        if 'promo' in request.data:
            instance.promo_id = request.data.get('promo')

        # Gambar hanya diubah jika dikirim
        if 'gambar' in request.FILES:
            instance.gambar = request.FILES['gambar']

        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DataView(APIView):
    def get(self, request):
        return Response({"pesan": "Halo dari backend Django!"})



class KasirTransaksiView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Untuk mendukung upload gambar bukti

    def post(self, request):
        serializer = TransHCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Transaksi berhasil disimpan."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagihanStokCreateView(generics.CreateAPIView):
    serializer_class = TagihanStokSerializer
    permission_classes = [IsAuthenticated]

class TransaksiShopViewSet(viewsets.ModelViewSet):
    queryset = TransaksiShop.objects.all()
    serializer_class = TransaksiShopSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class StokMasukView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'admin':
            queryset = StokMasuk.objects.all()
        else:
            return Response({"detail": "Hanya admin yang bisa melihat data stok masuk."}, status=403)

        serializer = StokMasukSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if user.role != 'admin':
            return Response({"detail": "Hanya admin yang bisa menambahkan stok."}, status=403)

        serializer = StokMasukSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(suplayer=user)  # Simpan user admin sebagai pencatat stok
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
