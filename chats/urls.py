from django.urls import path

from .views import index, question_add, comment_add, like, hashtag, questions, search

urlpatterns = [
    path('', index, name='index'),
    path('add_question/', question_add, name='question_add'),
    path('quests/', questions, name='questions'),
    path('search/', search, name='search'),
    path('add_comment/<int:question_id>/', comment_add, name='comment_add'),
    path('like/<int:pk>/', like, name='like'),
    path('hashtag/<str:hashtag>/', hashtag, name='hashtag'),
]


