from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
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

    def get_queryset(self):
        if self.action in ('list', 'retrieve', 'create'):
            queryset = Post.objects.filter(is_deleted=False).prefetch_related('hashtags')
        elif self.action in ('update', 'destroy'):
            queryset = Post.objects.filter(user=self.request.user, is_deleted=False).prefetch_related('hashtags')
        else:
            queryset = Post.objects.filter(user=self.request.user).prefetch_related('hashtags')
        return queryset

    def perform_destroy(self, instance):
        # instance.hashtags.clear()
        instance.is_deleted = True
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.hit()
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def recovery(self, request, **kwargs):
        instance = self.get_object()
        if instance.is_deleted:
            instance.is_deleted = False
            # for tag in instance.hashtags.all()[:]:
            #     instance.hashtags.add(tag)
            instance.save()
            return Response({"message": "성공적으로 복구하였습니다."}, status.HTTP_200_OK, content_type='json')
        else:
            return Response({"ERROR": "삭제되지 않은 게시글입니다."}, status.HTTP_400_BAD_REQUEST, content_type='json')

    @action(detail=True, methods=['put'])
    def like(self, request, **kwargs):
        instance = self.get_object()
        if self.request.user in instance.likes.all():
            instance.likes.remove(self.request.user)
            data = {"message": "좋아요 취소"}
        else:
            instance.likes.add(self.request.user)
            data = {"message": "좋아요"}
        return Response(data, status.HTTP_200_OK, content_type='json')
