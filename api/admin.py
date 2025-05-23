from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Ikan  # Import model Ikan juga

# Daftarkan model User dengan UserAdmin
admin.site.register(User, UserAdmin)

# Daftarkan model Ikan agar muncul di Django Admin
@admin.register(Ikan)
class IkanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'harga', 'stok', 'last_updated')
    search_fields = ('nama',)
    list_filter = ('last_updated',)
