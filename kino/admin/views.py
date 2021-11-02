from django.shortcuts import render


def statistics(request):
    return render(request, 'admin/statistics.html')


def banners(request):
    return render(request, 'admin/banners.html')


def movies(request):
    return render(request, 'admin/movies.html')


def cinemas(request):
    return render(request, 'admin/cinemas.html')


def news(request):
    return render(request, 'admin/news.html')


def promotion(request):
    return render(request, 'admin/promotion.html')


def pages(request):
    return render(request, 'admin/pages.html')


def users(request):
    return render(request, 'admin/users.html')


def mailing(request):
    return render(request, 'admin/mailing.html')
