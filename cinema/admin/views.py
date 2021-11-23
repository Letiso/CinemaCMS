from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, View
from django.contrib.auth import get_user_model
from .forms import ExtendedUserUpdateForm, TopBannerFormSet, BackgroundImageFormSet, NewsBannerFormSet
from django.http import HttpResponseRedirect


def statistics(request):
    context = {
        'title': 'Статистика',
    }
    return render(request, 'admin/statistics.html', context)


# region Banners
class BannersView(View):

    def get(self, request):
        context = {
            'forms': {
                'top_banners': TopBannerFormSet(request.POST or None, request.FILES or None, prefix='top_banners'),
                'background': BackgroundImageFormSet(request.POST or None, request.FILES or None, prefix='background'),
                'news_banners': NewsBannerFormSet(request.POST or None, request.FILES or None, prefix='news_banners'),
            },
        }
        return render(request, 'admin/banners/index.html', context)

    def post(self, request):
        context = {
            'forms': {
                'top_banners': TopBannerFormSet(request.POST or None, request.FILES or None, prefix='top_banners'),
                'background': BackgroundImageFormSet(request.POST or None, request.FILES or None, prefix='background'),
                'news_banners': NewsBannerFormSet(request.POST or None, request.FILES or None, prefix='news_banners'),
            },
        }

        def get_current_form():
            forms = list(context['forms'])
            for key in forms:
                if key in request.POST:
                    return context['forms'][key]

        formset = get_current_form()
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('banners')
        return render(request, 'admin/banners/index.html', context)


# endregion Banners


def movies(request):
    context = {
        'title': 'Фильмы',
    }
    return render(request, 'admin/movies.html', context)


def cinemas(request):
    context = {
        'title': 'Кинотеатры',
    }
    return render(request, 'admin/cinemas.html', context)


def news(request):
    context = {
        'title': 'Новости',
    }
    return render(request, 'admin/news.html', context)


def promotion(request):
    context = {
        'title': 'Акции',
    }
    return render(request, 'admin/promotion.html', context)


def pages(request):
    context = {
        'title': 'Страницы',
    }
    return render(request, 'admin/pages.html', context)


# region User
def users(request):
    context = {
        'title': 'Пользователи',
        'fields': ['ID', 'Ред./Удал.', 'Логин', 'Email', 'Номер телефона',
                   'Имя', 'Фамилия', 'Пол', 'Язык', 'Дата рождения', 'Адрес', 'Был(а)',
                   'Регистрация', 'Сотрудник', 'Админ', ],
        'users': get_user_model().objects.all(),
    }

    return render(request, 'admin/users/users.html', context)


class UserUpdateView(UpdateView):
    model = get_user_model()
    success_url = '/admin/users'
    template_name = 'admin/users/update.html'

    form_class = ExtendedUserUpdateForm


class UserDeleteView(View):

    @staticmethod
    def get(request, pk):
        model = get_user_model()
        user_to_delete = get_object_or_404(model, pk=pk)
        user_to_delete.delete()
        return redirect('users')


# endregion User


def mailing(request):
    context = {
        'title': 'Рассылка',
    }
    return render(request, 'admin/mailing.html', context)
