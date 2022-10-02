from django.db import models
from django.conf import settings


class Post(models.Model):
    """ 게시글 모델 """
    USER = settings.AUTH_USER_MODEL
    user = models.ForeignKey(USER, on_delete=models.DO_NOTHING, db_column='user_id')
    title = models.CharField(verbose_name='내용', max_length=255)
    content = models.CharField(verbose_name='내용', max_length=255)
    views = models.PositiveIntegerField(verbose_name='조회수', default=0)
    created_at = models.DateTimeField(verbose_name='생성 시각', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정 시각', auto_now=True)
    hashtags = models.ManyToManyField('HashTag', blank=True, related_name='posts')
    likes = models.ManyToManyField('User', blank=True, related_name='liked_posts')

    def count_likes(self):
        return self.likes.count()

    def hit(self):
        self.views += 1
        self.save()


class HashTag(models.Model):
    content = models.CharField(verbose_name='태그', max_length=20, unique=True)

    def __str__(self):
        return self.content

    def count_posts(self):
        return self.posts.count()
