from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.models import Produk
from .views import ProdukViewSet, RegisterView, LoginView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'produk', ProdukViewSet, basename='produk')

urlpatterns = [
    path('', include(router.urls)),

    # Auth user
    path('account/register/', RegisterView.as_view()),
    path('account/login/', LoginView.as_view()),
    path('account/token/refresh/', TokenRefreshView.as_view()),
    path('account/profile/', ProfileView.as_view()),
]

urlpatterns = [
    path('kategori/', views.KategoriListCreate.as_view()),
    path('promo/', views.PromoListCreate.as_view()),
    path('pembayaran/', views.PembayaranListCreate.as_view()),
    path('transaksi-h/', views.TransHListCreate.as_view()),
    path('transaksi-d/', views.TransDListCreate.as_view()),
]
