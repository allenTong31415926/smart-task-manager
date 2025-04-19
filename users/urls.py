from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LoginView

urlpatterns = [
    # RESTful authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Keep the old login endpoint for backward compatibility if needed
    # path('login/', LoginView.as_view(), name='login'),
]
