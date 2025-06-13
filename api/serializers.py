from rest_framework import serializers
from .models import User, Kategori, Promo, Produk, Pembayaran, Trans_h, Trans_d
from .models import Produk, Kategori, Promo

from rest_framework_simplejwt.views import TokenObtainPairView


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'konsumen')
        )
        
        return user

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'

from .models import Produk, Kategori, Promo

class ProdukSerializer(serializers.ModelSerializer):
    kategori = serializers.StringRelatedField(read_only=True)
    kategori_id = serializers.PrimaryKeyRelatedField(
        queryset=Kategori.objects.all(), source='kategori', write_only=True
    )

    promo = serializers.StringRelatedField(read_only=True)  # ⬅️ ubah jadi lowercase "promo"
    promo_id = serializers.PrimaryKeyRelatedField(
        queryset=Promo.objects.all(), source='promo', write_only=True
    )

    gambar = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Produk
        fields = [
            'id', 'nama', 'harga', 'stok', 'deskripsi',
            'kategori', 'kategori_id',
            'promo', 'promo_id',
            'gambar', 'last_updated'
        ]

    def create(self, validated_data):
        validated_data.pop('kategori', None)
        validated_data.pop('promo', None)
        return Produk.objects.create(**validated_data)


class PembayaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pembayaran
        fields = '__all__'

class TransHSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trans_h
        fields = '__all__'

class TransDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trans_d
        fields = '__all__'