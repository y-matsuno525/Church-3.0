from django.urls import path,include
from . import views

app_name = "menu"

urlpatterns = [
    path('',views.menu,name='menu'),
    path('get_verses/',views.get_verses,name='get_verses'),
    path('get_verse_annotations/',views.get_verse_annotations,name='get_verse_annotations'),
    path('add_verse_annotation/',views.add_verse_annotation,name='add_verse_annotation'),
    path('verse_questions/',views.verse_questions,name='verse_questions'),
    path('create_verse_question/',views.create_verse_question,name='create_verse_question'),
    path('register_verse_question/',views.register_verse_question,name='register_verse_question'),
    path('answer_verse_question/',views.answer_verse_question,name='answer_verse_question'),
    path('add_verse_answer/',views.add_verse_answer,name='add_verse_answer'),
]
