from django.urls import path
from . import views

urlpatterns = [
    path('', views.statistics, name="statistics"),
    path('banners', views.BannersView.as_view(), name="banners"),
    path('banner_image_validation', views.BannerImageValidationView.as_view(), name="banner_image_validation"),
    path('movies', views.movies, name="movies"),
    path('cinemas', views.cinemas, name="cinemas_conf"),
    path('news', views.news, name="news_conf"),
    path('promotion', views.promotion, name="promotion_conf"),
    path('pages', views.pages, name="pages"),
    path('users', views.users, name="users"),
    path('users/<int:pk>/update', views.UserUpdateView.as_view(), name="update_user"),
    path('users/<int:pk>/delete', views.UserDeleteView.as_view(), name="delete_user"),
    path('mailing', views.mailing, name="mailing"),
    ]
