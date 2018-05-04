from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    path('answers/<int:pk>/', views.CreatCommentView.as_view(), name='post_comment'),
    path('<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete'),
    path('answer/<int:pk>/', views.CommentsListView.as_view(), name='list'),
]
