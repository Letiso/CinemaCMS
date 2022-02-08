from django.urls import path
from . import views

urlpatterns = [
    path('', views.StatisticsView.as_view(), name="statistics"),

    path('banners', views.BannersView.as_view(), name="banners"),

    path('movies', views.MoviesView.as_view(), name="movies"),
    path('movie_card/<str:pk>', views.MovieCardView.as_view(), name="movie_card"),
    path('movie_card/<str:pk>/delete', views.MovieCardDeleteView.as_view(), name="delete_movie_card"),

    path('cinemas', views.CinemasView.as_view(), name="cinemas_conf"),
    path('cinema_card/<str:pk>', views.CinemaCardView.as_view(), name="cinema_card"),
    path('cinema_card/<str:pk>/delete', views.CinemaCardDeleteView.as_view(), name="delete_cinema_card"),

    path('cinema/<str:cinema_pk>/hall_card/<str:pk>/', views.CinemaHallCardView.as_view(), name="hall_card"),
    path('cinema/<str:cinema_pk>/hall_card/<str:pk>/delete', views.CinemaHallCardDeleteView.as_view(), name="delete_hall_card"),

    path('movie_sessions/<str:pk>/halls', views.CinemasView.as_view(), name="movie_sessions"),

    path('news', views.NewsView.as_view(), name="news_conf"),
    path('news_card/<str:pk>', views.NewsCardView.as_view(), name="news_card"),
    path('news_card/<int:pk>/delete', views.NewsCardDeleteView.as_view(), name="delete_news"),

    path('promotion', views.PromotionListView.as_view(), name="promotion_conf"),
    path('promotion_card/<str:pk>', views.PromotionCardView.as_view(), name="promotion_card"),
    path('promotion_card/<int:pk>/delete', views.PromotionCardDeleteView.as_view(), name="delete_promotion"),

    path('pages', views.PageListView.as_view(), name="pages"),
    path('pages/main_page_card', views.MainPageCardView.as_view(), name="main_page_card"),
    path('pages/page_card/<str:pk>', views.PageCardView.as_view(), name="page_card"),
    path('pages/page_card/<int:pk>/delete', views.PageCardDeleteView.as_view(), name="delete_page"),
    path('pages/contacts_page_card', views.ContactsPageCardView.as_view(), name="contacts_page_card"),

    path('users', views.UsersListView.as_view(), name="users"),
    path('user/<int:pk>/update', views.UserUpdateView.as_view(), name="update_user"),
    path('user/<int:pk>/delete', views.UserDeleteView.as_view(), name="delete_user"),

    path('mailing', views.MailingView.as_view(), name="mailing"),
    ]
