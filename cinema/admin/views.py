import json

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, View
from django.contrib.auth import get_user_model
from .forms import (
    ExtendedUserUpdateForm,
    TopBannerFormSet, BackgroundImageForm, NewsBannerFormSet, BannersCarouselForm
)
from django.http import HttpResponseRedirect, JsonResponse


def statistics(request):
    context = {
        'title': 'Статистика',
    }
    return render(request, 'admin/statistics.html', context)


# region Banners
class BannerImageValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        image = data['image'].image
        width, height = 2000, 3000
        if not image or image.image.size != (width, height):
            return JsonResponse({'image_error': f'Выберите изображение с разрешением {width}x{height}'})
        return JsonResponse({'image_valid': True})


class BannersView(View):

    @staticmethod
    def get_instance(model, prefix=None):
        # {'name': prefix} using for get_or_create BannersCarousel instances
        # {'pk': 1} using for get_or_create BackgroundImage singleton-instance
        key = {'name': prefix} if prefix else {'pk': 1}
        instance, created = model.objects.get_or_create(**key)
        return instance

    def get_context(self):
        return {
            'top_banners': {
                'formset': TopBannerFormSet(prefix='top_banners'),
                'carousel': BannersCarouselForm(
                    instance=self.get_instance(BannersCarouselForm.Meta.model, 'top_banners'), prefix='top_banners')
            },

            'background_image': BackgroundImageForm(
                instance=self.get_instance(BackgroundImageForm.Meta.model), prefix='background_image'),

            'news_banners': {
                'formset': NewsBannerFormSet(prefix='news_banners'),
                'carousel': BannersCarouselForm(
                    instance=self.get_instance(BannersCarouselForm.Meta.model, 'news_banners'), prefix='news_banners')
            },
        }

    def get(self, request):
        return render(request, 'admin/banners/index.html', self.get_context())

    def post(self, request):
        context = self.get_context()

        def get_current_form(context):
            for name in context.keys():
                if name in request.POST:
                    if 'formset' in context[name]:
                        formset, carousel = context[name]['formset'], context[name]['carousel']

                        formset = formset.__class__(request.POST, request.FILES, prefix=name)
                        carousel = carousel.__class__(request.POST, request.FILES,
                                                      instance=carousel.instance, prefix=name)
                        return formset, carousel
                    else:
                        context[name] = context[name].__class__(request.POST, request.FILES,
                                                                instance=context[name].instance, prefix=name)
                        return context[name],

        forms = get_current_form(context)
        if False not in [form.is_valid() for form in forms]:
            for form in forms:
                form.save()
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
