from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, View
from django.contrib.auth import get_user_model
from .forms import (
    ExtendedUserUpdateForm,
    TopBannerFormSet, BackgroundImageForm, NewsBannerFormSet, BannersCarouselForm,
    MovieCardForm, MovieFrameFormset
)

from django.http import HttpResponseRedirect


def statistics(request):
    context = {
        'title': 'Статистика',
    }
    return render(request, 'admin/statistics.html', context)


# region Banners
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
                'required_size': TopBannerFormSet.model.required_size,
                'formset': TopBannerFormSet(prefix='top_banners'),
                'carousel': BannersCarouselForm(
                    instance=self.get_instance(BannersCarouselForm.Meta.model, 'top_banners'), prefix='top_banners')
            },

            'background_image': {
                'required_size': BackgroundImageForm.Meta.model.required_size,
                'form': BackgroundImageForm(
                    instance=self.get_instance(BackgroundImageForm.Meta.model), prefix='background_image'),
            },
            'news_banners': {
                'required_size': TopBannerFormSet.model.required_size,
                'formset': NewsBannerFormSet(prefix='news_banners'),
                'carousel': BannersCarouselForm(
                    instance=self.get_instance(BannersCarouselForm.Meta.model, 'news_banners'), prefix='news_banners')
            },
        }

    def get(self, request):
        return render(request, 'admin/banners/index.html', self.get_context())

    def post(self, request):
        context = self.get_context()

        def get_current_form():
            for name in context.keys():
                if name in request.POST:
                    if 'formset' in context[name]:
                        formset, carousel = context[name]['formset'], context[name]['carousel']

                        context[name]['formset'] = formset.__class__(request.POST, request.FILES, prefix=name)
                        context[name]['carousel'] = carousel.__class__(request.POST, request.FILES,
                                                                       instance=carousel.instance, prefix=name)
                        return context[name]['formset'], context[name]['carousel']
                    else:
                        context[name]['form'] = context[name]['form'].__class__(request.POST, request.FILES,
                                                                                instance=context[name]['form'].instance,
                                                                                prefix=name)
                        return context[name]['form'],

        forms = get_current_form()
        if False not in [form.is_valid() for form in forms]:
            for form in forms:
                form.save()
            return HttpResponseRedirect('banners')

        return render(request, 'admin/banners/index.html', context)


# endregion Banners

# region Movies
class MoviesView(View):
    context = {
        'title': 'Фильмы',
        'releases': MovieCardForm.Meta.model.objects.filter(is_active=True),
        'announcements': MovieCardForm.Meta.model.objects.filter(is_active=False),
    }

    def get(self, request):
        return render(request, 'admin/movies/index.html', self.context)


class MovieCardView(View):

    def get_context(self, request, pk: str):
        return {
            'form': MovieCardForm(request.POST or None, request.FILES or None,
                                  instance=get_object_or_404(MovieCardForm.Meta.model, pk=int(pk))
                                  if pk.isdigit() else None,
                                  prefix='movie'),
            'gallery': MovieFrameFormset(request.POST or None, request.FILES or None,
                                         prefix='movie_frames',
                                         queryset=MovieFrameFormset.model.objects.filter(movie_id=int(pk))
                                         if pk.isdigit() else MovieFrameFormset.model.objects.none()),
            'required_size': MovieFrameFormset.model.required_size,
        }

    def get(self, request, pk: str):
        return render(request, 'admin/movies/movie_card.html', self.get_context(request, pk))

    def post(self, request, pk: str):
        context = self.get_context(request, pk)
        movie, gallery = context['form'], context['gallery']

        if False not in [movie.is_valid(), gallery.is_valid()]:
            movie.save()

            for movie_frame in gallery:
                if movie_frame.is_valid():
                    movie_frame = movie_frame.save(commit=False)
                    movie_frame.movie = movie.instance
            gallery.save()

            return redirect(f'movie_card', pk=movie.instance.pk)

        return render(request, 'admin/movies/movie_card.html', context)

# endregion Movies


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
