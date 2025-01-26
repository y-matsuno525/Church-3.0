from django.db import models
from django.contrib.auth.models import User

class Bible(models.Model):
    LANGUAGE_CHOICES = [
        ("ja", "日本語"),
        ("en", "英語"),
    ]

    version = models.CharField(max_length=100)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return f"{self.version} ({dict(self.LANGUAGE_CHOICES).get(self.language, 'Unknown')})"

class Book(models.Model):
    bible = models.ForeignKey(Bible, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.book.name} Chapter {self.chapter_number}"
    
    def previous_chapter(self):
        return Chapter.objects.filter(book=self.book, chapter_number__lt=self.chapter_number).order_by('-chapter_number').first()

    def next_chapter(self):
        return Chapter.objects.filter(book=self.book, chapter_number__gt=self.chapter_number).order_by('chapter_number').first()

class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    verse_number = models.PositiveIntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.chapter.book.name} {self.chapter.chapter_number}:{self.verse_number}"
    
class VerseFavorite(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorite by {self.user.username} on verse {self.verse.id}"

class VerseAnnotation(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return f"Annotation by {self.user.username} on {self.verse.id}"

class VerseAnnotationFavorite(models.Model):
    annotation = models.ForeignKey(VerseAnnotation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorite by {self.user.username} on annotation {self.annotation.id}"

class VerseQuestion(models.Model):
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE, related_name="verse")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question by {self.user.username} on {self.verse.id}"

class VerseAnswer(models.Model):
    question = models.ForeignKey(VerseQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username} on question {self.question.id}"

class VerseAnswerFavorite(models.Model):
    answer = models.ForeignKey(VerseAnswer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorite by {self.user.username} on answer {self.answer.id}"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    annotation = models.ForeignKey(VerseAnnotation, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(VerseQuestion, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Tagged {self.tag.name}"
