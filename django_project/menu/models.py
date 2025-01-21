from django.db import models

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