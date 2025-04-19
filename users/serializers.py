from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

# LoginSerializer is no longer needed as we're using TokenObtainPairView
# You can add other serializers here as needed
