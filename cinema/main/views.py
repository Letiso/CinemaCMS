from django.shortcuts import render, get_object_or_404
from .models import *

def get_or_none(model, pk):
    try: return model.objects.get(pk=pk)
    except model.DoesNotExist: pass


def index(request):
    context = {
        'top_banners': {
            'banners': TopBanner.objects.filter(is_active=True),
            'active_slide': TopBanner.objects.first(),
            'carousel': get_or_none(BannersCarousel, pk=1),
        },

        'background_image': get_or_none(BackgroundImage, pk=1),

        'news_banners': {
            'banners': NewsBanner.objects.filter(is_active=True),
            'carousel': get_or_none(BannersCarousel, pk=2),
            'active_slide': NewsBanner.objects.first()
        },
    }
    return render(request, 'main/index.html', context)


def poster(request):
    context = {
        'title': 'Фильмы',
        'releases': MovieCard.objects.filter(is_active=True),
        'announcements': MovieCard.objects.filter(is_active=False),
    }
    return render(request, 'main/poster/poster.html', context)


def movie_card(request):
    return render(request, 'main/poster/movie_card.html')


def soon(request):
    return render(request, 'main/soon.html')


def timetable(request):
    return render(request, 'main/timetable/timetable.html')


def ticket_booking(request):
    return render(request, 'main/timetable/ticket_booking.html')


def cinemas(request):
    return render(request, 'main/cinemas/cinemas.html')


def cinema_card(request):
    return render(request, 'main/cinemas/cinema_card.html')


def hall_card(request):
    return render(request, 'main/cinemas/hall_card.html')


def promotion(request):
    return render(request, 'main/promotion/promotion.html')


def promotion_card(request):
    return render(request, 'main/promotion/promotion_card.html')


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


def user_account(request):
    return render(request, 'main/user_account.html')
