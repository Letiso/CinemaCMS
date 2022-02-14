from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse

from .models import *


# region Mixins
class CustomAbstractView(View):
    template_name:str = None
    context:dict = None

    @staticmethod
    def get_context(*args, **kwargs) -> dict:
        return {}

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.context = self.get_context(request, *args, **kwargs)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name, self.context)


# endregion Mixins

#region MainPage
class MainPageView(CustomAbstractView):
    template_name = 'main/index.html'

    @staticmethod
    def get_top_banners_context():
        banners = TopBanner.objects.filter(is_active=True)
        active_slide = TopBanner.objects.first()
        carousel = BannersCarousel.objects.filter(pk=1).first()

        return {'banners': banners, 'active_slide': active_slide, 'carousel': carousel}

    @staticmethod
    def get_background_image_context():
        background_image = BackgroundImage.objects.filter(pk=1).first()

        return {'background_image': background_image}

    @staticmethod
    def get_news_banners_context():
        banners = NewsBanner.objects.filter(is_active=True)
        active_slide = NewsBanner.objects.first()
        carousel = BackgroundImage.objects.filter(pk=2).first()

        return {'banners': banners, 'active_slide': active_slide, 'carousel': carousel}

    def get_context(self, request):
        self.context = super().get_context()

        self.context['top_banners'] = self.get_top_banners_context()
        self.context['background_image'] = self.get_background_image_context()

        self.context['news_banners'] = self.get_news_banners_context()

        return self.context


# endregion MainPage

# region Poster
def poster(request):
    context = {
        'title': 'Фильмы',
        'releases': MovieCard.objects.filter(is_active=True),
        'announcements': MovieCard.objects.filter(is_active=False),
    }
    return render(request, 'main/poster/poster.html', context)


# endregion Poster

# region Soon
def soon(request):
    return render(request, 'main/soon.html')


# endregion Soon

# region MovieCard
def movie_card(request):
    return render(request, 'main/poster/movie_card.html')


# endregion MovieCard

# region Timetable
def timetable(request):
    return render(request, 'main/timetable/timetable.html')


# endregion Timetable

# region TicketBooking
def ticket_booking(request):
    return render(request, 'main/timetable/ticket_booking.html')


# endregion TicketBooking

# region Cinemas
def cinemas(request):
    return render(request, 'main/cinemas/cinemas.html')


def cinema_card(request):
    return render(request, 'main/cinemas/cinema_card.html')


def hall_card(request):
    return render(request, 'main/cinemas/hall_card.html')


# endregion Cinemas

# region Promotion
def promotion(request):
    return render(request, 'main/promotion/promotion.html')


def promotion_card(request):
    return render(request, 'main/promotion/promotion_card.html')


# endregion Promotion

# region Pages
def about_the_cinema(request):
    return render(request, 'main/about_the_cinema/about_the_cinema.html')


def advertising(request):
    return render(request, 'main/about_the_cinema/advertising.html')


def cafe_bar(request):
    return render(request, 'main/about_the_cinema/cafe_bar.html')


def child_room(request):
    return render(request, 'main/about_the_cinema/child_room.html')


def contacts(request):
    return render(request, 'main/about_the_cinema/contacts.html')


def mobile_applications(request):
    return render(request, 'main/about_the_cinema/mobile_applications.html')


def news(request):
    return render(request, 'main/about_the_cinema/news.html')


def vip_hall(request):
    return render(request, 'main/about_the_cinema/vip_hall.html')


# endregion Pages
