from django.db import models
from django.contrib.auth.models import AbstractUser

# Model untuk User dengan role
class User(AbstractUser):
    role = models.CharField(max_length=50, default='pembeli')

# Model untuk Ikan
class Ikan(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    stok = models.IntegerField()
    deskripsi = models.TextField(blank=True, null=True)
    gambar = models.ImageField(upload_to='gambar_ikan/', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama
