from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .backends import CustomModelBackend

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Create an instance of our custom backend
            backend = CustomModelBackend()
            user = backend.authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

            refresh = self.get_token(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return data

        msg = 'Must include "username" and "password".'
        raise serializers.ValidationError(msg, code='authorization')

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {'access': str(refresh.access_token)}
        return data
