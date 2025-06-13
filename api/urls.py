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
    DataView
)

router = DefaultRouter()
router.register(r'produk', ProdukViewSet,)

urlpatterns = [
    path('', include(router.urls)),
    
    # Autentikasi
    path('account/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/register/', RegisterView.as_view(), name='register'),
    path('account/token/refresh/', TokenRefreshView.as_view()),
    path('account/profile/', ProfileView.as_view(),name='profile'),
    
    # Master Data
    path('kategori/', KategoriListCreate.as_view()),
    path('promo/', PromoListCreate.as_view()),
    path('pembayaran/', PembayaranListCreate.as_view()),
    
    # Transaksi
    path('transaksi-h/', TransHListCreate.as_view()),
    path('transaksi-d/', TransDListCreate.as_view()),
    
    # Test
    path('test/', DataView.as_view()),
]