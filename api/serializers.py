from rest_framework import serializers
from .models import User, Kategori, Promo, Produk, Pembayaran, Trans_h, Trans_d
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import TagihanStok
from .models import TransaksiShop
from .models import StokMasuk



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
    nama = serializers.CharField(source='nama_kategori')

    class Meta:
        model = Kategori
        fields = ['id', 'nama']

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ['id', 'nama']

class ProdukSerializer(serializers.ModelSerializer):
    jumlah = serializers.IntegerField(write_only=True, required=False)

    nama = serializers.CharField(required=False)
    harga = serializers.IntegerField(required=False)
    stok = serializers.IntegerField(required=False)
    deskripsi = serializers.CharField(required=False)

    kategori = KategoriSerializer(read_only=True)
    kategori_id = serializers.PrimaryKeyRelatedField(
        queryset=Kategori.objects.all(), source='kategori', write_only=True, required=False
    )

    promo = PromoSerializer(read_only=True)
    promo_id = serializers.PrimaryKeyRelatedField(
        queryset=Promo.objects.all(), source='promo', write_only=True, required=False
    )

    gambar = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Produk
        fields = [
            'id', 'nama', 'harga', 'stok', 'deskripsi',
            'kategori', 'kategori_id',
            'promo', 'promo_id',
            'gambar', 'last_updated',
            'jumlah'
        ]

    def create(self, validated_data):
        # Hapus 'jumlah' jika ada, karena bukan field model
        validated_data.pop('jumlah', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Tambah stok jika 'jumlah' dikirim (khusus halaman suplayer)
        request = self.context.get('request')
        if request and 'jumlah' in request.data:
            try:
                tambahan = int(request.data['jumlah'])
                instance.stok += tambahan
            except ValueError:
                raise serializers.ValidationError({"jumlah": "Harus berupa angka"})
        else:
            # Jika tidak pakai jumlah, update stok langsung (optional)
            instance.stok = validated_data.get('stok', instance.stok)

        # Update field lain
        instance.nama = validated_data.get('nama', instance.nama)
        instance.harga = validated_data.get('harga', instance.harga)
        instance.deskripsi = validated_data.get('deskripsi', instance.deskripsi)
        instance.kategori = validated_data.get('kategori', instance.kategori)
        instance.promo = validated_data.get('promo', instance.promo)

        if 'gambar' in validated_data:
            instance.gambar = validated_data['gambar']

        instance.save()
        return instance

        


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
        fields = ['produk', 'jumlah', 'total']

class TransHCreateSerializer(serializers.ModelSerializer):
    detail = TransDSerializer(many=True)

    class Meta:
        model = Trans_h
        fields = ['tanggal', 'konsumen', 'kasir', 'total', 'jenis_payment', 'bukti_pembayaran', 'detail']

    def create(self, validated_data):
        detail_data = validated_data.pop('detail')
        trans_h = Trans_h.objects.create(**validated_data)
        for item in detail_data:
            Trans_d.objects.create(transaksi=trans_h, **item)
        return trans_h

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_active:
            raise serializers.ValidationError("Akun tidak aktif.")

        requested_role = self.context['request'].data.get('actor')  # ambil dari request frontend
        if requested_role and user.role != requested_role:
            raise serializers.ValidationError("Role tidak sesuai.")

        # Kirim tambahan data ke frontend (Laravel)
        data['role'] = user.role
        data['username'] = user.username
        data['id'] = user.id

        return data
    
class TagihanStokSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagihanStok
        fields = '__all__'

class TransaksiShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransaksiShop
        fields = '__all__'

    def create(self, validated_data):
        produk = validated_data['produk']
        jumlah = validated_data['jumlah']

        if produk.stok < jumlah:
            raise serializers.ValidationError({"jumlah": "Stok tidak mencukupi."})

        produk.stok -= jumlah
        produk.save()

        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if instance.bukti_transfer and hasattr(instance.bukti_transfer, 'url') and request:
            data['bukti_transfer'] = request.build_absolute_uri(instance.bukti_transfer.url)
        
        return data



class StokMasukSerializer(serializers.ModelSerializer):
    nama_produk = serializers.CharField(source='produk.nama', read_only=True)
    nama_suplayer = serializers.CharField(source='suplayer.username', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = StokMasuk
        fields = ['id', 'produk', 'nama_produk', 'suplayer', 'nama_suplayer', 'tanggal_masuk', 'jumlah', 'harga_satuan', 'keterangan', 'subtotal']
        read_only_fields = ['suplayer']

    def get_subtotal(self, obj):
        return obj.jumlah * obj.harga_satuan

    def create(self, validated_data):
        # Tambahkan stok ke produk saat menyimpan stok masuk
        produk = validated_data['produk']
        jumlah = validated_data['jumlah']

        # Tambahkan stok
        produk.stok += jumlah
        produk.save()

        # Simpan entri StokMasuk
        stok_masuk = StokMasuk.objects.create(**validated_data)
        return stok_masuk
