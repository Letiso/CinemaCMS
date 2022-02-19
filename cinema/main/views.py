from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponse

from itertools import chain

from .models import *


# region Mixins
class CustomAbstractView(View):
    template_name: str = None
    context: dict = None

    @staticmethod
    def get_context(*args, **kwargs) -> dict:
        main_page_card = MainPageCard.objects.filter(pk=1).first()
        navbar_phone_numbers = main_page_card.get_phone_numbers()

        return {'navbar_phone_numbers': navbar_phone_numbers}

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.context = self.get_context(request, *args, **kwargs)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name, self.context)


# endregion Mixins

# region MainPage
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
class MoviesPosterView(CustomAbstractView):
    template_name = 'main/poster/poster.html'

    def get_context(self, request):
        self.context = super().get_context()

        self.context['releases'] = MovieCard.objects.filter(is_active=True)
        self.context['announcements'] = MovieCard.objects.filter(is_active=False)

        return self.context


class MovieCardView(CustomAbstractView):
    template_name = 'main/poster/movie_card.html'


# endregion Poster

# region Soon
class MoviesSoonView(CustomAbstractView):
    template_name = 'main/soon.html'


# endregion Soon

# region Timetable
class MovieSessionsTimetableView(CustomAbstractView):
    template_name = 'main/timetable/timetable.html'


class TicketBookingView(CustomAbstractView):
    template_name = 'main/timetable/ticket_booking.html'


# endregion Timetable

# region Cinemas
class CinemasView(CustomAbstractView):
    template_name = 'main/cinemas/index.html'

    def get_context(self, request):
        self.context = super().get_context()

        self.context['cinemas'] = CinemaCard.objects.filter(is_active=True)
        self.context['context_ads'] = list(range(3))  # just for empty ads render

        return self.context


class CinemaCardView(CustomAbstractView):
    template_name = 'main/cinemas/cinema_card.html'

    def get_context(self, request, pk):
        self.context = super().get_context()

        cinema = get_object_or_404(CinemaCard, pk=pk)
        self.context['cinema'] = cinema

        self.context['halls'] = cinema.halls.all()
        self.context['gallery'] = cinema.gallery.all()
        self.context['movie_sessions'] = list(range(6))

        return self.context


class HallCardView(CustomAbstractView):
    template_name = 'main/cinemas/hall_card.html'

    def get_context(self, request, pk):
        self.context = super().get_context()

        hall = get_object_or_404(CinemaHallCard, pk=pk)
        self.context['hall'] = hall
        self.context['gallery'] = hall.gallery.all()
        self.context['movie_sessions'] = list(range(6))

        return self.context


# endregion Cinemas

# region Promotion
class PromotionView(CustomAbstractView):
    template_name = 'main/promotion/index.html'

    def get_context(self, request):
        self.context = super().get_context()

        self.context['promotions'] = PromotionCard.objects.filter(is_active=True)
        self.context['context_ads'] = list(range(3))  # just for empty ads render

        return self.context


class PromotionCardView(CustomAbstractView):
    template_name = 'main/promotion/promotion_card.html'

    def get_context(self, request, pk):
        self.context = super().get_context()

        promotion = get_object_or_404(PromotionCard, pk=pk)
        self.context['promotion'] = promotion
        self.context['gallery'] = promotion.gallery.all()
        self.context['context_ads'] = list(range(3))  # just for empty ads render

        return self.context


# endregion Promotion

# region Pages
class AboutTheCinemaPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/about_the_cinema.html'

    def get_context(self, request, pk=1):
        self.context = super().get_context()

        page_card = get_object_or_404(AboutTheCinemaPageCard, pk=pk)
        self.context['page_card'] = page_card
        self.context['context_ads'] = list(range(3))

        return self.context


class AdvertisingPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/advertising.html'


class CafeBarPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/cafe_bar.html'


class ChildRoomPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/child_room.html'


class ContactsPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/contacts.html'


class MobileApplicationsPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/mobile_applications.html'


class NewsPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/news.html'


class VipHallPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/vip_hall.html'


# endregion Pages
