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
    @staticmethod
    def get_context():
        return {
            'formsets': {
                'top_banners': TopBannerFormSet(prefix='top_banners'),
                'background': BackgroundImageFormSet(prefix='background'),
                'news_banners': NewsBannerFormSet(prefix='news_banners'),
            },
        }

    def get(self, request):
        return render(request, 'admin/banners/index.html', self.get_context())

    def post(self, request):
        context = self.get_context()

        def get_current_formset(formsets):
            formset_names = list(formsets)
            for name in formset_names:
                if name in request.POST:
                    formsets[name] = formsets[name].__class__(request.POST, request.FILES, prefix=name)
                    return formsets[name]

        formset = get_current_formset(context['formsets'])
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
