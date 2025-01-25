from django.contrib import admin
from .models import Bible,Book,Chapter,Verse,VerseAnnotation,VerseAnnotationFavorite,VerseFavorite,VerseQuestion,VerseAnswer,VerseAnswerFavorite

# Register your models here.
admin.site.register(Bible)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Verse)
admin.site.register(VerseAnnotation)
admin.site.register(VerseAnnotationFavorite)
admin.site.register(VerseFavorite)
admin.site.register(VerseQuestion)
admin.site.register(VerseAnswer)
admin.site.register(VerseAnswerFavorite)