from django.urls import path
from . import views

urlpatterns = [
    path('', views.statistics, name="statistics"),
    path('banners', views.banners, name="banners"),
    path('movies', views.movies, name="movies"),
    path('cinemas', views.cinemas, name="cinemas"),
    path('news', views.news, name="news"),
    path('promotion', views.promotion, name="promotion"),
    path('pages', views.pages, name="pages"),
    path('users', views.users, name="users"),
    path('mailing', views.mailing, name="mailing"),
    ]
