"""fakeZhihu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from users import views as users_views
from asks import views as asks_views
from answers import views as answers_views
from topics import views as topics_view

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users_views.IndexView.as_view(), name='index'),
    path('login/', users_views.login, name='login'),
    path('logout/', users_views.logout, name='logout'),
    path('register/', users_views.register, name='register'),
    path('explore/', answers_views.IndexView.as_view(), name='explore'),
    path('topics/', include('topics.urls')),
    path('users/', include('users.urls')),
    path('asks/', include('asks.urls')),
    path('answers/', include('answers.urls')),
    path('comments/', include('comments.urls')),
    path('api/', include(router.urls)),
    path('docs/', include_docs_urls('知乎'))
]
