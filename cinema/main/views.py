from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView
from django.http import HttpResponse

from .models import *


# region Mixins
class CustomAbstractView(View):
    template_name: str = None
    context: dict = None

    @staticmethod
    def get_context(*args, **kwargs) -> dict:
        main_page_card = MainPageCard.objects.filter(pk=1).first()
        navbar_phone_numbers = main_page_card.get_phone_numbers()

        return {'main_page_card': main_page_card, 'navbar_phone_numbers': navbar_phone_numbers}

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
class MoviesPosterView(ListView):
    template_name = 'main/poster/index.html'
    paginate_by = 18
    model = MovieSession
    
    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(
            start_datetime__gt=timezone.now()
        ).order_by('-start_datetime').select_related()
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        main_page_card = MainPageCard.objects.filter(pk=1).first()
        context['navbar_phone_numbers'] = main_page_card.get_phone_numbers()

        context['context_ads'] = list(range(3))  # just for empty ads render

        return context


class MovieCardView(CustomAbstractView):
    template_name = 'main/poster/movie_card.html'


# endregion Poster

# region Soon
class MoviesSoonView(MoviesPosterView):
    template_name = 'main/poster/soon.html'
    model = MovieCard

    def get_queryset(self):
        queryset = super(ListView, self).get_queryset()

        return queryset.filter(
            release_date__gt=timezone.now()
        ).order_by('-release_date').select_related()

# endregion Soon


# region Timetable
class MovieSessionsTimetableView(CustomAbstractView):
    template_name = 'main/timetable/timetable.html'


class TicketBookingView(CustomAbstractView):
    template_name = 'main/timetable/ticket_booking.html'


# endregion Timetable

# region Cinemas
class CinemasListView(ListView):
    template_name = 'main/cinemas/index.html'
    paginate_by = 10
    model = CinemaCard

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        main_page_card = MainPageCard.objects.filter(pk=1).first()
        context['navbar_phone_numbers'] = main_page_card.get_phone_numbers()

        context['context_ads'] = list(range(3))  # just for empty ads render

        return context


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
class PromotionListView(ListView):
    template_name = 'main/promotion/index.html'
    paginate_by = 10
    model = PromotionCard

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        main_page_card = MainPageCard.objects.filter(pk=1).first()
        context['navbar_phone_numbers'] = main_page_card.get_phone_numbers()

        context['context_ads'] = list(range(3))  # just for empty ads render

        return context


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

    def get_context(self, request, pk='4') -> dict:
        self.context = super().get_context()

        page = get_object_or_404(PageCard, pk=pk)
        self.context['page'] = page
        self.context['gallery'] = page.gallery.all()

        self.context['context_ads'] = list(range(3))  # just for empty ads render

        return self.context


class CafeBarPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/cafe_bar.html'

    def get_context(self, request, pk='1') -> dict:
        self.context = super().get_context()

        page = get_object_or_404(PageCard, pk=pk)
        self.context['page'] = page
        self.context['gallery'] = page.gallery.all()

        self.context['context_ads'] = list(range(3))  # just for empty ads render

        return self.context


class ChildRoomPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/child_room.html'

    def get_context(self, request, pk='3') -> dict:
        self.context = super().get_context()

        page = get_object_or_404(PageCard, pk=pk)
        self.context['page'] = page
        self.context['gallery'] = page.gallery.all()

        self.context['context_ads'] = list(range(3))  # just for empty ads render

        return self.context


class ContactsPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/contacts.html'

    def get_context(self, request, pk=1) -> dict:
        self.context = super().get_context()

        contacts = ContactsPageCard.objects.filter(is_active=True)
        self.context['contacts'] = contacts

        self.context['context_ads'] = list(range(3))  # just for empty ads render

        return self.context


class MobileApplicationsPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/mobile_applications.html'

    def get_context(self, request, pk=1):
        self.context = super().get_context()

        self.context['context_ads'] = list(range(3))  # just for empty ads render

        return self.context


class NewsListView(ListView):
    template_name = 'main/about_the_cinema/news/index.html'
    paginate_by = 10
    model = NewsCard

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        main_page_card = MainPageCard.objects.filter(pk=1).first()
        context['navbar_phone_numbers'] = main_page_card.get_phone_numbers()

        context['context_ads'] = list(range(3))  # just for empty ads render

        return context


class NewsCardView(CustomAbstractView):
    template_name = 'main/about_the_cinema/news/news_card.html'

    def get_context(self, request, pk):
        self.context = super().get_context()

        news = get_object_or_404(NewsCard, pk=pk)
        self.context['news'] = news
        self.context['gallery'] = news.gallery.all()
        self.context['context_ads'] = list(range(3))  # just for empty ads render

        return self.context


class VipHallPageView(CustomAbstractView):
    template_name = 'main/about_the_cinema/vip_hall.html'

    def get_context(self, request, pk='2') -> dict:
        self.context = super().get_context()

        page = get_object_or_404(PageCard, pk=pk)
        self.context['page'] = page
        self.context['gallery'] = page.gallery.all()

        self.context['context_ads'] = list(range(3))  # just for empty ads render

        return self.context


# endregion Pages
