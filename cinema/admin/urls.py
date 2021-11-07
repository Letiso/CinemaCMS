from django.urls import path
from . import views

urlpatterns = [
    path('', views.statistics, name="statistics"),
    path('banners', views.banners, name="banners"),
    path('movies', views.movies, name="movies"),
    path('cinemas', views.cinemas, name="cinemas_conf"),
    path('news', views.news, name="news_conf"),
    path('promotion', views.promotion, name="promotion_conf"),
    path('pages', views.pages, name="pages"),
    path('users', views.users, name="users"),
    path('mailing', views.mailing, name="mailing"),
    ]
