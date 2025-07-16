from operator import truediv
from pickle import TRUE
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import DateField
from django.contrib.auth import get_user_model

# Model untuk User dengan role
class User(AbstractUser):
    role = models.CharField(max_length=50, default='konsumen',choices=[('admin','Admin'),('kasir','Kasir'),('konsumen','Konsumen'),('suplayer','Suplayer')])

#model class 
class Kategori (models.Model):
    nama_kategori = models.CharField(max_length=50, null=True)
    keterangan = models.TextField(max_length=100, null=True,blank=True) 
    
    def __str__(self):
        return self.nama_kategori or ""

class Promo (models.Model):
    nama = models.CharField(max_length=100,null=True)
    tglm = models.DateField(null=True)
    tgla = models.DateField(null=True)
    persen = models.DecimalField(decimal_places=3,max_digits=10) 
    
    def __str__(self):
        return self.nama 

# Model untuk produk 
class Produk(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.IntegerField()
    deskripsi = models.TextField(blank=True, null=True)
    gambar = models.ImageField(upload_to='gambar_ikan/', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    kategori = models.ForeignKey(Kategori, null=True, on_delete=models.SET_NULL)
    promo = models.ForeignKey(Promo, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nama
    
class Pembayaran(models.Model):
    nama_pembayaran = models.CharField(max_length=50, null=True)
    keterangan = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nama_pembayaran or ""

class Trans_h(models.Model):
    tanggal = models.DateField()
    konsumen = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='konsumen_transaksi')
    kasir = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='kasir_transaksi')
    total = models.DecimalField(decimal_places=2, max_digits=10)
    jenis_payment = models.ForeignKey(Pembayaran, on_delete=models.CASCADE, null=True)
    bukti_pembayaran = models.ImageField(upload_to='bukti_pembayaran/', null=True, blank=True)

class Trans_d(models.Model):
    transaksi = models.ForeignKey(Trans_h, on_delete=models.CASCADE, related_name='detail')
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE, null=True)
    jumlah = models.IntegerField(null=True)
    total = models.DecimalField(decimal_places=2, max_digits=10)

class TagihanStok(models.Model):
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tagihan_supplier")
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    harga_satuan = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    tanggal = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='menunggu')  # menunggu / disetujui / ditolak
    keterangan = models.TextField(blank=True, null=True)



class TransaksiShop(models.Model):
    produk = models.ForeignKey('Produk', on_delete=models.CASCADE)
    nama_pembeli = models.CharField(max_length=100)
    jumlah = models.PositiveIntegerField()
    total_harga = models.DecimalField(max_digits=12, decimal_places=2)
    metode_pembayaran = models.CharField(max_length=20, choices=[('qris', 'QRIS'), ('transfer', 'Transfer')])
    bukti_transfer = models.ImageField(upload_to='bukti_transfer/', null=True, blank=True)
    status_pembayaran = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('terverifikasi', 'Terverifikasi')], default='pending')
    tanggal = models.DateTimeField(auto_now_add=True)
    lokasi_pengantaran = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"{self.nama_pembeli} - {self.produk.nama}"
    User = get_user_model()


class StokMasuk(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    suplayer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'suplayer'})
    tanggal_masuk = models.DateField()
    jumlah = models.PositiveIntegerField()
    harga_satuan = models.DecimalField(max_digits=10, decimal_places=2)
    keterangan = models.TextField(blank=True, null=True)

    @property
    def subtotal(self):
        return self.jumlah * self.harga_satuan

