from rest_framework import serializers
from .models import User,Kategori, Promo, Produk, Pembayaran, Trans_h, Trans_d
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from .models import Produk

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data.get('role', 'pembeli')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produk
        fields = '__all__'

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'

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