from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
    ValidationError)
from .models import Post, HashTag
import re


class PostSerializer(ModelSerializer):
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
        return obj.count_likes()

    def get_hashtag(self, obj):
        tag = ""
        for tag_value in obj.hashtags.values_list('content', flat=True):
            tag += f'#{tag_value}'
        return tag

    def validate_tags(self, value):
        p = re.compile(r'^#[가-힣A-Za-z0-9]+')
        values = value.split(",")
        for v in values:
            if not p.match(v):
                raise ValidationError("ERROR: 태그 형식이 올바르지 않습니다.")
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        tags_list = tags.split(",")
        user = self.context['request'].user
        post = self.Meta.model.objects.create(user=user, **validated_data)

        for tag in tags_list:
            _tag, _ = HashTag.objects.get_or_create(content=tag[1:])
            _tag.posts.add(post)

        return post

    def update(self, instance, validated_data):
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
