from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
    ValidationError)
from .models import Post, HashTag
import re


class PostSerializer(ModelSerializer):
    """ 게시글 Serializer """
    tags = CharField(write_only=True, )
    like = SerializerMethodField()
    hashtag = SerializerMethodField()

    class Meta:
        model = Post
        fields = ('user', 'title', 'content',
                  'views', 'created_at', 'updated_at',
                  'tags', 'like', 'hashtag', 'is_deleted')
        read_only_fields = ('user', 'hashtag', 'views', 'created_at', 'updated_at', 'like')

    def get_like(self, obj):
        """ 좋아요 수 반환 함수 """
        return obj.count_likes()

    def get_hashtag(self, obj):
        """ 해시태그 반환 함수 """
        tag = ""
        for tag_value in obj.hashtags.values_list('content', flat=True):
            tag += f'#{tag_value}'
        return tag

    def validate_tags(self, value):
        """ 해시태그 validate 함수 """
        # ','로 구분했을 때 각각의 원소는 '#글자혹은숫자' 형식이어야 함
        p = re.compile(r'^#[가-힣A-Za-z0-9]+')
        values = value.split(",")
        for v in values:
            if not p.match(v):
                raise ValidationError("ERROR: 태그 형식이 올바르지 않습니다.")
        return value

    def create(self, validated_data):
        """ post 생성 함수 """
        tags = validated_data.pop('tags')
        tags_list = tags.split(",")
        user = self.context['request'].user
        post = self.Meta.model.objects.create(user=user, **validated_data)

        for tag in tags_list:
            _tag, _ = HashTag.objects.get_or_create(content=tag[1:])
            _tag.posts.add(post)

        return post

    def update(self, instance, validated_data):
        """ post 수정 함수 """
        # 기존 태그를 모두 지우고 다시 연결
        instance.hashtags.clear()
        tags = validated_data.pop('tags')
        tags_list = tags.split(",")
        for tag in tags_list:
            _tag, _ = HashTag.objects.get_or_create(content=tag[1:])
            _tag.posts.add(instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
