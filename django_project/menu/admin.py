from django.contrib import admin
from .models import Bible,Book,Chapter,Verse

# Register your models here.
admin.site.register(Bible)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Verse)