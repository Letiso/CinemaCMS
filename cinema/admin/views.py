from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, View
from django.contrib.auth import get_user_model
from .forms import (
    ExtendedUserUpdateForm,
    TopBannerFormSet, BackgroundImageForm, NewsBannerFormSet, BannersCarouselForm,
    MovieCardForm, MovieFrameFormset
)

from django.http import HttpResponseRedirect


# region Statistics
def statistics(request):
    context = {
        'title': 'Статистика',
    }
    return render(request, 'admin/statistics.html', context)


# endregion Statistics

# region Banners
class BannersView(View):

    @staticmethod
    def get_instance(model, prefix: str = None):
        """
        {'name': prefix} using for get_or_create BannersCarousel instances
        {'pk': 1} using for get_or_create BackgroundImage singleton-instance
        """
        instance_key = {'name': prefix} if prefix else {'pk': 1}

        instance, created = model.objects.get_or_create(**instance_key)
        return instance

    def get_context(self, request) -> dict:
        return {
            'top_banners': {
                'required_size': TopBannerFormSet.model.required_size,
                'formset': TopBannerFormSet(request.POST or None, request.FILES or None, prefix='top_banners'),
                'carousel': BannersCarouselForm(request.POST or None,
                                                instance=self.get_instance(BannersCarouselForm.Meta.model,
                                                                           'top_banners'), prefix='top_banners')
            },

            'background_image': {
                'required_size': BackgroundImageForm.Meta.model.required_size,
                'form': BackgroundImageForm(request.POST or None, request.FILES or None,
                                            instance=self.get_instance(BackgroundImageForm.Meta.model),
                                            prefix='background_image'),
            },
            'news_banners': {
                'required_size': TopBannerFormSet.model.required_size,
                'formset': NewsBannerFormSet(request.POST or None, request.FILES or None, prefix='news_banners'),
                'carousel': BannersCarouselForm(request.POST or None,
                                                instance=self.get_instance(BannersCarouselForm.Meta.model,
                                                                           'news_banners'), prefix='news_banners')
            },
        }

    def get(self, request):
        return render(request, 'admin/banners/index.html', self.get_context(request))

    def post(self, request):
        context = self.get_context(request)

        def get_current_form() -> tuple:
            for name in context.keys():
                if name in request.POST:
                    return context[name]['formset'], context[name]['carousel'] if 'formset' in context[name] \
                        else context[name]['form'],

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
            'movie': {
                'form': MovieCardForm(request.POST or None, request.FILES or None,
                                      instance=get_object_or_404(MovieCardForm.Meta.model, pk=int(pk))
                                      if pk.isdigit() else None,
                                      prefix='movie'),
                'required_size': MovieCardForm.Meta.model.required_size,
            },
            'gallery': {
                'formset': MovieFrameFormset(request.POST or None, request.FILES or None,
                                             prefix='movie_frames',
                                             queryset=MovieFrameFormset.model.objects.filter(movie_id=int(pk))
                                             if pk.isdigit() else MovieFrameFormset.model.objects.none()),
                'required_size': MovieFrameFormset.model.required_size,
            }
        }

    def get(self, request, pk: str):
        return render(request, 'admin/movies/movie_card.html', self.get_context(request, pk))

    def post(self, request, pk: str):
        context = self.get_context(request, pk)
        movie, gallery = context['movie']['form'], context['gallery']['formset']

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

# region Cinemas
def cinemas(request):
    context = {
        'title': 'Кинотеатры',
    }
    return render(request, 'admin/cinemas.html', context)


# endregion Cinemas

# region News
def news(request):
    context = {
        'title': 'Новости',
    }
    return render(request, 'admin/news.html', context)


# endregion News

# region Promotion
def promotion(request):
    context = {
        'title': 'Акции',
    }
    return render(request, 'admin/promotion.html', context)


# endregion Promotion

# region Pages
def pages(request):
    context = {
        'title': 'Страницы',
    }
    return render(request, 'admin/pages.html', context)


# endregion Pages

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

# region Mailing
def mailing(request):
    context = {
        'title': 'Рассылка',
    }
    return render(request, 'admin/mailing.html', context)
# endregion Mailing
