from django.urls import path,include
from . import views

app_name = "menu"

urlpatterns = [
    path('',views.menu,name='menu'),
    path('get_verses/',views.get_verses,name='get_verses'),
    path('get_forum_posts/',views.get_forum_posts,name='get_forum_posts'),
]
