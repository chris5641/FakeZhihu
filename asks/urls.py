from django.urls import path

from . import views
from answers import views as answers_views

app_name = 'asks'
urlpatterns = [
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/answer/<int:answer_id>/', views.AnswerDetailView.as_view(), name='answer_detail'),
    path('<int:pk>/answers/', answers_views.CreateAnswerView.as_view(), name='post_answer'),
    path('<int:pk>/follow/', views.follow_ask, name='follow'),
    path('<int:pk>/unfollow/', views.unfollow_ask, name='unfollow'),
    path('', views.CreateAskView.as_view(), name='post_ask'),
]
