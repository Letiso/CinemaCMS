from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.MainPageView.as_view(), name="main_page"),

    path('poster', views.MoviesPosterView.as_view(), name="poster"),
    path('poster/movie_card/<int:pk>', views.MovieCardView.as_view(), name="movie_card"),

    path('soon', views.MoviesSoonView.as_view(), name="soon"),

    path('timetable', views.MovieSessionsTimetableView.as_view(), name="timetable"),
    *[
        path(f'timetable/movie_id=<int:movie_id>{optional_parameter}',
             views.MovieSessionsTimetableView.as_view(), name="timetable") for optional_parameter in (
            '', '/movie_type=<str:movie_type>', '/start_date=<str:start_date>',
            '/movie_type=<str:movie_type>/hall_id=<int:hall_id>')
      ],
    path('timetable/ticket_booking/<int:pk>', views.TicketBookingView.as_view(), name="ticket_booking"),

    path('cinemas', views.CinemasListView.as_view(), name="cinemas"),
    path('cinemas/cinema_card/<int:pk>', views.CinemaCardView.as_view(), name="cinema_card"),
    path('cinemas/hall_card/<int:pk>', views.HallCardView.as_view(), name="hall_card"),

    path('promotion', views.PromotionListView.as_view(), name="promotion"),
    path('promotion/promotion_card/<int:pk>', views.PromotionCardView.as_view(), name="promotion_card"),

    path('about_the_cinema', views.AboutTheCinemaPageView.as_view(), name="about_the_cinema"),

    path('about_the_cinema/news', views.NewsListView.as_view(), name="news"),
    path('about_the_cinema/news/<int:pk>', views.NewsCardView.as_view(), name="news_card"),

    path('about_the_cinema/advertising', views.AdvertisingPageView.as_view(), name="advertising"),
    path('about_the_cinema/vip_hall', views.VipHallPageView.as_view(), name="vip_hall"),
    path('about_the_cinema/cafe_bar', views.CafeBarPageView.as_view(), name="cafe_bar"),
    path('about_the_cinema/child_room', views.ChildRoomPageView.as_view(), name="child_room"),
    path('about_the_cinema/mobile_applications', views.MobileApplicationsPageView.as_view(),
         name="mobile_applications"),
    path('about_the_cinema/contacts', views.ContactsPageView.as_view(), name="contacts"),
]
