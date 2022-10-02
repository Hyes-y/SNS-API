from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer
from .models import Post, HashTag


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().prefetch_related('hashtags')
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'create'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_destroy(self, instance):
        instance.hashtags.clear()
        instance.delete()
