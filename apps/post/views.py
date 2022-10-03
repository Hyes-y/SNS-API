from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsOwnerOrReadOnly
from .paginations import CustomPageNumberPagination
from .serializers import PostSerializer
from .models import Post
from django.db.models import Count


class PostViewSet(ModelViewSet):
    """ 게시글 CRUD API """
    queryset = Post.objects.all().prefetch_related('hashtags')
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'likes', 'views']
    ordering = ['-created_at']

    def get_permissions(self):
        """ permission 반환 함수 : action별 권한 설정 """
        if self.action in ('update', 'destroy', 'recovery'):
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """ queryset 반환 함수 : 태그 필터링 포함 """
        if self.action in ('list', 'retrieve', 'create'):
            params = self.request.query_params.get('tags', None)
            if params:
                # 태그 필터링
                params = params.split(",")
                queryset = \
                    Post.objects\
                        .filter(is_deleted=False, hashtags__content__in=params)\
                        .annotate(tag_cnt=Count('id'))\
                        .filter(tag_cnt=len(params))
            else:
                queryset = Post.objects.filter(is_deleted=False).prefetch_related('hashtags')

        elif self.action in ('update', 'destroy'):
            queryset = Post.objects.filter(user=self.request.user, is_deleted=False).prefetch_related('hashtags')

        else:
            # 삭제된 게시글 복구하는 경우
            queryset = Post.objects.filter(user=self.request.user).prefetch_related('hashtags')

        return queryset

    def perform_destroy(self, instance):
        """
        게시글 삭제
        is_deleted: True 로 변경
        """
        # instance.hashtags.clear()
        instance.is_deleted = True
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        """
        게시글 조회
        조회시 hit()를 통해 조회수 증가
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.hit()
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def recovery(self, request, **kwargs):
        """
        삭제된 게시글 복구 action
        is_deleted: False 로 변경
        """
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
        """
        좋아요 기능
        좋아요 요청시 이미 좋아요 데이터가 있는 경우 좋아요 취소
        없는 경우 데이터 추가
        """
        instance = self.get_object()
        if self.request.user in instance.likes.all():
            instance.likes.remove(self.request.user)
            data = {"message": "좋아요 취소"}
        else:
            instance.likes.add(self.request.user)
            data = {"message": "좋아요"}
        return Response(data, status.HTTP_200_OK, content_type='json')
