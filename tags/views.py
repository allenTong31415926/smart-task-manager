from rest_framework import viewsets, permissions
from .models import Tag
from .serializers import TagSerializer

class TagViewSet(viewsets.ReadOnlyModelViewSet):  # Read-only for now
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
