from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, View
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Model

from .forms import (
    ExtendedUserUpdateForm,
    TopBannerFormSet, BackgroundImageForm, NewsBannerFormSet, BannersCarouselForm,
    MovieCardForm, MovieFrameFormset,
    NewsCardForm, NewsGalleryFormset,
    SEOForm
)

from datetime import date


# region Statistics
def statistics(request) -> HttpResponse:
    context = {
        'title': 'Статистика',
    }
    return render(request, 'admin/statistics.html', context)


# endregion Statistics

# region Banners
class BannersView(View):

    @staticmethod
    def get_instance(model, prefix: str = None) -> Model:
        """
        {'name': prefix} using for get_or_create BannersCarousel instances
        {'pk': 1} using for get_or_create BackgroundImage singleton-instance
        """
        instance_key = {'name': prefix} if prefix else {'pk': 1}

        instance, created = model.objects.get_or_create(**instance_key)
        return instance

    def get_context(self, request) -> dict:
        def try_to_bound(name) -> dict:
            return {'data': request.POST, 'files': request.FILES, } if name in request.POST else {}

        return {
            'top_banners': {
                'required_size': TopBannerFormSet.model.required_size,
                'formset': TopBannerFormSet(**try_to_bound('top_banners'), prefix='top_banners'),
                'carousel': BannersCarouselForm(**try_to_bound('top_banners'),
                                                instance=self.get_instance(BannersCarouselForm.Meta.model,
                                                                           'top_banners'), prefix='top_banners')
            },
            'background_image': {
                'required_size': BackgroundImageForm.Meta.model.required_size,
                'form': BackgroundImageForm(**try_to_bound('background_image'),
                                            instance=self.get_instance(BackgroundImageForm.Meta.model),
                                            prefix='background_image'),
            },
            'news_banners': {
                'required_size': TopBannerFormSet.model.required_size,
                'formset': NewsBannerFormSet(**try_to_bound('news_banners'), prefix='news_banners'),
                'carousel': BannersCarouselForm(**try_to_bound('news_banners'),
                                                instance=self.get_instance(BannersCarouselForm.Meta.model,
                                                                           'news_banners'), prefix='news_banners')
            },
        }

    def get(self, request) -> HttpResponse:
        return render(request, 'admin/banners/index.html', self.get_context(request))

    def post(self, request) -> HttpResponse:
        context = self.get_context(request)

        def get_current_form() -> tuple:
            for name in context.keys():
                if name in request.POST:
                    return (context[name]['formset'], context[name]['carousel']) \
                        if 'formset' in context[name] else (context[name]['form'],)

        forms = get_current_form()
        if False not in [form.is_valid() for form in forms]:
            for form in forms:
                form.save()
            return HttpResponseRedirect('banners')

        return render(request, 'admin/banners/index.html', context)


# endregion Banners

# region Movies
class MoviesView(View):
    @staticmethod
    def get_context() -> dict:
        order = '-date_created'
        return {
            'title': 'Фильмы',
            'releases': MovieCardForm.Meta.model.objects.filter(is_active=True,
                                                                release_date__lte=date.today()).order_by(order),
            'announcements': MovieCardForm.Meta.model.objects.filter(is_active=True,
                                                                     release_date__gt=date.today()).order_by(order),
            'inactive_cards': MovieCardForm.Meta.model.objects.exclude(is_active=True).order_by(order),
        }

    def get(self, request) -> HttpResponse:
        return render(request, 'admin/movies/index.html', self.get_context())


class MovieCardView(View):

    @staticmethod
    def get_context(request, pk: str) -> dict:
        return {
            'pk': pk,
            'title': 'Карточка фильма',
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
            },
            'seo': {
                'form': SEOForm(request.POST or None,
                                instance=get_object_or_404(SEOForm.Meta.model, movie_id=int(pk))
                                if pk.isdigit() else None,
                                prefix='seo'),
            },
            'currentUrl': request.get_full_path(),
        }

    def get(self, request, pk: str) -> HttpResponse:
        return render(request, 'admin/movies/movie_card.html', self.get_context(request, pk))

    def post(self, request, pk: str) -> HttpResponse:
        context = self.get_context(request, pk)
        movie, gallery, seo = context['movie']['form'], context['gallery']['formset'], context['seo']['form']

        if False not in [movie.is_valid(), gallery.is_valid(), seo.is_valid()]:
            movie.save()

            for movie_frame in gallery:
                if movie_frame.is_valid():
                    movie_frame = movie_frame.save(commit=False)
                    movie_frame.movie = movie.instance
            gallery.save()

            seo = seo.save(commit=False)
            seo.movie = movie.instance
            seo.save()

            return redirect('movies')

        return render(request, 'admin/movies/movie_card.html', context)


# endregion Movies

# region Cinemas
def cinemas(request) -> HttpResponse:
    context = {
        'title': 'Кинотеатры',
    }
    return render(request, 'admin/cinemas.html', context)


# endregion Cinemas

# region News
class NewsView(View):
    @staticmethod
    def get_context() -> dict:
        return {
            'title': 'Новости',
            'table_labels': ['ID', 'Название', 'Дата создания', 'Статус', 'Редактировать'],
            'news': NewsCardForm.Meta.model.objects.all(),
        }

    def get(self, request) -> HttpResponse:
        return render(request, 'admin/news/index.html', self.get_context())


class NewsCardView(View):

    @staticmethod
    def get_context(request, pk: str) -> dict:
        return {
            'pk': pk,
            'title': 'Карточка новости',
            'news': {
                'form': NewsCardForm(request.POST or None, request.FILES or None,
                                     instance=get_object_or_404(NewsCardForm.Meta.model, pk=int(pk))
                                     if pk.isdigit() else None,
                                     prefix='news'),
                'required_size': NewsCardForm.Meta.model.required_size,
            },
            'gallery': {
                'formset': NewsGalleryFormset(request.POST or None, request.FILES or None,
                                              prefix='news_image',
                                              queryset=NewsGalleryFormset.model.objects.filter(news_id=int(pk))
                                              if pk.isdigit() else NewsGalleryFormset.model.objects.none()),
                'required_size': NewsGalleryFormset.model.required_size,
            },
            'seo': {
                'form': SEOForm(request.POST or None,
                                instance=get_object_or_404(SEOForm.Meta.model, news_id=int(pk))
                                if pk.isdigit() else None,
                                prefix='seo'),
            },
            'currentUrl': request.get_full_path(),
        }

    def get(self, request, pk: str) -> HttpResponse:
        return render(request, 'admin/news/news_card.html', self.get_context(request, pk))

    def post(self, request, pk: str) -> HttpResponse:
        context = self.get_context(request, pk)
        news, gallery, seo = context['news']['form'], context['gallery']['formset'], context['seo']['form']

        if False not in [news.is_valid(), gallery.is_valid(), seo.is_valid()]:
            news.save()

            for news_image in gallery:
                if news_image.is_valid():
                    news_image = news_image.save(commit=False)
                    news_image.movie = news.instance
            gallery.save()

            seo = seo.save(commit=False)
            seo.news = news.instance
            seo.save()

            return redirect('news')

        return render(request, 'admin/news/index.html', context)


# endregion News

# region Promotion
def promotion(request) -> HttpResponse:
    context = {
        'title': 'Акции',
    }
    return render(request, 'admin/promotion.html', context)


# endregion Promotion

# region Pages
def pages(request) -> HttpResponse:
    context = {
        'title': 'Страницы',
    }
    return render(request, 'admin/pages.html', context)


# endregion Pages

# region User
class UsersView(View):
    @staticmethod
    def get_context():
        return {
            'title': 'Пользователи',
            'table_labels': ['ID', 'Логин', 'Email', 'Номер телефона',
                             'Имя', 'Фамилия', 'Пол', 'Язык', 'Дата рождения', 'Адрес', 'Был(а)',
                             'Регистрация', 'Сотрудник', 'Админ', 'Ред.'],
            'users': get_user_model().objects.all(),
        }

    def get(self, request) -> HttpResponse:
        return render(request, 'admin/users/users.html', self.get_context())


class UserUpdateView(UpdateView):
    model = get_user_model()
    success_url = '/admin/users'
    template_name = 'admin/users/update.html'

    form_class = ExtendedUserUpdateForm


class UserDeleteView(View):

    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        model = get_user_model()
        user_to_delete = get_object_or_404(model, pk=pk)
        user_to_delete.delete()
        return redirect('users')


# endregion User

# region Mailing
def mailing(request) -> HttpResponse:
    context = {
        'title': 'Рассылка',
    }
    return render(request, 'admin/mailing.html', context)
# endregion Mailing
