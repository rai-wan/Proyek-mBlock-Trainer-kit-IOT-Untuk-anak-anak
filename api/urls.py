from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IkanViewSet, RegisterView, LoginView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'ikan', IkanViewSet, basename='ikan')

urlpatterns = [
    path('', include(router.urls)),

    # Auth user
    path('account/register/', RegisterView.as_view()),
    path('account/login/', LoginView.as_view()),
    path('account/token/refresh/', TokenRefreshView.as_view()),
    path('account/profile/', ProfileView.as_view()),
]

