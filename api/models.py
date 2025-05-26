from operator import truediv
from pickle import TRUE
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import DateField

# Model untuk User dengan role
class User(AbstractUser):
    role = models.CharField(max_length=50, default='konsumen',choices=[('admin','Admin'),('kasir','Kasir'),('konsumen','Konsumen'),('Suplayer','Suplayer')])

#model class 
class Kategori (models.Model):
    nama_kategori = models.CharField(max_length=50, null=True)
    keterangan = models.TextField(max_length=100, null=True,blank=True) 
    
    def __str__(self):
        return self.nama_kategori

class Promo (models.Model):
    nama = models.CharField(max_length=100,null=True)
    tglm = models.DateField(null=True)
    tgla = models.DateField(null=True)
    persen = models.DecimalField(decimal_places=3,max_digits=10)  

# Model untuk produk 
class Produk(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.IntegerField()
    deskripsi = models.TextField(blank=True, null=True)
    ketegori = models.ForeignKey(Kategori,on_delete=models.CASCADE,null=True)
    gambar = models.ImageField(upload_to='gambar_ikan/', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    Promo = models.ForeignKey(Promo,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.nama
    
class Pembayaran (models.Model): 
    nama_pembayaran = models.CharField(max_length=50, null=True)
    keterangan = models.TextField(max_length=100, null=True,blank=True)

class Trans_h (models.Model):
    tanggal = models.DateField()
    konsumen = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='konsumen')
    kasir = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='kasir')
    total = models.DecimalField(decimal_places=2,max_digits=10)
    jenis_payment = models.ForeignKey(Pembayaran, on_delete=models.CASCADE,null=True)

class Trans_d (models.Model):
    produk = models.ForeignKey(Produk,on_delete=models.CASCADE,null=True)
    jumlah = models.IntegerField(null=True)
    total = models.DecimalField(decimal_places=2,max_digits=10)


