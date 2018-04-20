from django.urls import path

from . import views

app_name = 'answers'
urlpatterns = [
    path('<int:pk>/voteup/', views.vote_up, name='voteup'),
    path('<int:pk>/votedown/', views.vote_down, name='votedown'),
    path('<int:pk>/content/', views.ShowAnswerView.as_view(), name='content'),
    # path('<int:pk>/delete/', views.delete_answer, name='delete'),
    path('<int:pk>/delete/', views.DeleteAnswerView.as_view(), name='delete'),
]
