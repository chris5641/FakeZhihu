from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('setting/', views.PasswordView.as_view(), name='setting'),
    path('<int:pk>/answers/', views.AnswerView.as_view(), name='answers'),
    path('<int:pk>/asks/', views.AskView.as_view(), name='asks'),
    path('<int:pk>/collections/', views.CollectionView.as_view(), name='collections'),
    path('<int:pk>/following/', views.FollowingView.as_view(), name='following'),
    path('<int:pk>/followers/', views.FollowerView.as_view(), name='followers'),
    path('<int:pk>/following/asks/', views.FollowAskView.as_view(), name='follow_asks'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    path('unfollow/<int:pk>/', views.unfollow, name='unfollow'),
]
