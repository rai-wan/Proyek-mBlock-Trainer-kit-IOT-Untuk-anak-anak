from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ProdukViewSet,
    RegisterView,
    MyTokenObtainPairView,
    ProfileView,
    KategoriListCreate,
    PromoListCreate,
    PembayaranListCreate,
    TransHListCreate,
    TransDListCreate,
    DataView,
    TagihanStokCreateView,
    TransaksiShopViewSet,
    KasirTransaksiView,
    StokMasukView,
)

# ✅ Gunakan hanya satu router
router = DefaultRouter()
router.register(r'produk', ProdukViewSet)
router.register(r'shop-transaksi', TransaksiShopViewSet, basename='shop-transaksi')

urlpatterns = [
    path('', include(router.urls)),

    # Auth
    path('account/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/register/', RegisterView.as_view(), name='register'),
    path('account/token/refresh/', TokenRefreshView.as_view()),
    path('account/profile/', ProfileView.as_view(), name='profile'),

    # Master Data
    path('kategori/', KategoriListCreate.as_view()),
    path('promo/', PromoListCreate.as_view()),
    path('pembayaran/', PembayaranListCreate.as_view()),

    # Transaksi
    path('transaksi-h/', TransHListCreate.as_view()),
    path('transaksi-d/', TransDListCreate.as_view()),
    path('kasir/transaksi/', KasirTransaksiView.as_view(), name='kasir-transaksi'),
    path('tagihan-stok/', TagihanStokCreateView.as_view(), name='tagihan-stok'),

    # Test
    path('test/', DataView.as_view()),

     path('stok-masuk/', StokMasukView.as_view()),
]
