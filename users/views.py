from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

# LoginView is no longer needed as we're using TokenObtainPairView
# You can add other user-related views here, such as:
# - User registration
# - User profile management
# - Password reset
# etc.
