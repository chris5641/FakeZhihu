from django.urls import path

from . import views
from .models import Comment

app_name = 'comments'
urlpatterns = [
    path('answers/<int:pk>/', views.CreatCommentView.as_view(), name='post_comment'),
    path('<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete'),
]
