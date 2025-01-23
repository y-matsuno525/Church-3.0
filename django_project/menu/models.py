from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bible(models.Model):

    LANGUAGE_CHOICES = {
        # 言語コード : 表示される表示（日本語）
        "ja": "日本語",
        "en": "英語",
    }

    version = models.CharField(max_length=100)
    language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES)

class Book(models.Model):
    bible = models.ForeignKey(Bible, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()

class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    verse_number = models.IntegerField()
    text = models.TextField()

class ForumPost(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 投稿者
    content = models.TextField()  # 投稿の内容
    created_at = models.DateTimeField(auto_now_add=True)  # 投稿日時

class Favorite(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # お気に入りしたユーザー
    created_at = models.DateTimeField(auto_now_add=True)  # お気に入りした日時

    class Meta:
        unique_together = ('post', 'user')  # ユーザーは1つの投稿を1回だけお気に入りできる

    def __str__(self):
        return f"Favorite by {self.user.username} for Post {self.post.id}"