from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, DeleteView, View
from django.contrib.auth import get_user_model
from .forms import ExtendedUserUpdateForm  # , UpdateUserProfileForm


def statistics(request):
    context = {
        'title': 'Статистика',
    }
    return render(request, 'admin/statistics.html', context)


def banners(request):
    context = {
        'title': 'Банеры',
    }
    return render(request, 'admin/banners.html', context)


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


# def users(request):
#     context = {
#         'title': 'Пользователи',
#         'fields': ['ID', 'Ред./Удал.','Логин', 'Email', 'Номер телефона',
#                    'Имя', 'Фамилия', 'Пол', 'Язык', 'Дата рождения', 'Адрес', 'Был(а)',
#                    'Регистрация', 'Сотрудник', 'Админ', ],
#         'users': get_user_model().objects.all(),
#     }
#
#     return render(request, 'admin/users/users.html', context)

def users(request):
    context = {
        'title': 'Пользователи',
        'fields': ['ID', 'Ред./Удал.','Логин', 'Email', 'Номер телефона',
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


def mailing(request):
    context = {
        'title': 'Рассылка',
    }
    return render(request, 'admin/mailing.html', context)
