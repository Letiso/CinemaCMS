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
    PromotionCardForm, PromotionGalleryFormset,
    MainPageCardForm, PageCardForm, PageGalleryFormset, ContactsPageCardFormset,
    SEOForm
)

from datetime import date

from cinema.tasks import hello_world

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
            'news_list': NewsCardForm.Meta.model.objects.all(),
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
                    news_image.news = news.instance
            gallery.save()

            seo = seo.save(commit=False)
            seo.news = news.instance
            seo.save()

            return redirect('news_conf')

        return render(request, 'admin/news/index.html', context)


class NewsCardDeleteView(View):
    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        model = NewsCardForm.Meta.model
        news_to_delete = get_object_or_404(model, pk=pk)
        news_to_delete.delete()
        return redirect('news_conf')


# endregion News

# region Promotion
class PromotionListView(View):
    @staticmethod
    def get_context() -> dict:
        return {
            'title': 'Акции',
            'table_labels': ['ID', 'Название', 'Дата создания', 'Статус', 'Редактировать'],
            'promotion_list': PromotionCardForm.Meta.model.objects.all(),
        }

    def get(self, request) -> HttpResponse:
        return render(request, 'admin/promotion/index.html', self.get_context())


class PromotionCardView(View):

    @staticmethod
    def get_context(request, pk: str) -> dict:
        return {
            'pk': pk,
            'title': 'Карточка акции',
            'promotion': {
                'form': PromotionCardForm(request.POST or None, request.FILES or None,
                                          instance=get_object_or_404(PromotionCardForm.Meta.model, pk=int(pk))
                                          if pk.isdigit() else None,
                                          prefix='promotion'),
                'required_size': PromotionCardForm.Meta.model.required_size,
            },
            'gallery': {
                'formset': PromotionGalleryFormset(request.POST or None, request.FILES or None,
                                                   prefix='promotion_image',
                                                   queryset=PromotionGalleryFormset.model.objects.filter(
                                                       promotion_id=int(pk))
                                                   if pk.isdigit() else PromotionGalleryFormset.model.objects.none()),
                'required_size': PromotionGalleryFormset.model.required_size,
            },
            'seo': {
                'form': SEOForm(request.POST or None,
                                instance=get_object_or_404(SEOForm.Meta.model, promotion_id=int(pk))
                                if pk.isdigit() else None,
                                prefix='seo'),
            },
            'currentUrl': request.get_full_path(),
        }

    def get(self, request, pk: str) -> HttpResponse:
        return render(request, 'admin/promotion/promotion_card.html', self.get_context(request, pk))

    def post(self, request, pk: str) -> HttpResponse:
        context = self.get_context(request, pk)
        promotion, gallery, seo = context['promotion']['form'], context['gallery']['formset'], context['seo']['form']

        if False not in [promotion.is_valid(), gallery.is_valid(), seo.is_valid()]:
            promotion.save()

            for promotion_image in gallery:
                if promotion_image.is_valid():
                    promotion_image = promotion_image.save(commit=False)
                    promotion_image.promotion = promotion.instance
            gallery.save()

            seo = seo.save(commit=False)
            seo.promotion = promotion.instance
            seo.save()

            return redirect('promotion_conf')

        return render(request, 'admin/promotion/index.html', context)


class PromotionCardDeleteView(View):
    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        model = PromotionCardForm.Meta.model
        promotion_to_delete = get_object_or_404(model, pk=pk)
        promotion_to_delete.delete()
        return redirect('promotion_conf')


# endregion Promotion

# region Pages
class PageListView(View):
    @staticmethod
    def get_context() -> dict:
        primary_pages = ('О кинотеатре', 'Кафе - Бар', 'VIP - зал', 'Реклама', 'Детская комната', )

        return {
            'title': 'Страницы',
            'table_labels': ['Название', 'Дата создания', 'Статус', 'Редактировать'],
            'main_page': MainPageCardForm.Meta.model.objects.get_or_create(pk=1, title='Главная страница')[0],
            'primary_page_list': [
                PageCardForm.Meta.model.objects.get_or_create(pk=pk, title=title)[0]
                for pk, title in enumerate(primary_pages)
            ],
            'contacts_page': ContactsPageCardFormset.model.objects.get_or_create(pk=1, title='Контакты')[0],
            'custom_page_list': PageCardForm.Meta.model.objects.exclude(id__in=list(range(len(primary_pages)))),
        }

    def get(self, request) -> HttpResponse:
        hello_world.delay()
        return render(request, 'admin/pages/index.html', self.get_context())


class MainPageCardView(View):
    @staticmethod
    def get_context(request, pk=1) -> dict:
        return {
            'title': 'Карточка главной страницы',
            'page': {
                'form': MainPageCardForm(request.POST or None, request.FILES or None,
                                         instance=get_object_or_404(MainPageCardForm.Meta.model, pk=pk),
                                         prefix='main_page'),
            },
            'seo': {
                'form': SEOForm(request.POST or None,
                                instance=get_object_or_404(SEOForm.Meta.model, main_page_id=pk)
                                if SEOForm.Meta.model.objects.filter(main_page_id=pk).exists() else None,
                                prefix='seo'),
            },
            'currentUrl': request.get_full_path(),
        }

    def get(self, request) -> HttpResponse:
        return render(request, 'admin/pages/main_page_card.html', self.get_context(request))

    def post(self, request) -> HttpResponse:
        context = self.get_context(request, pk=1)
        page, seo = context['page']['form'], context['seo']['form']

        if False not in [page.is_valid(), seo.is_valid()]:
            page.save()

            seo = seo.save(commit=False)
            seo.main_page = page.instance
            seo.save()

            return redirect('pages')

        return render(request, 'admin/pages/index.html', context)


class PageCardView(View):

    @staticmethod
    def get_context(request, pk: str) -> dict:
        return {
            'pk': pk,
            'title': 'Карточка страницы',
            'page': {
                'form': PageCardForm(request.POST or None, request.FILES or None,
                                     instance=get_object_or_404(PageCardForm.Meta.model, pk=int(pk))
                                     if pk.isdigit() else None,
                                     prefix='page'),
                'required_size': PageCardForm.Meta.model.required_size,
            },
            'gallery': {
                'formset': PageGalleryFormset(request.POST or None, request.FILES or None,
                                              prefix='page_image',
                                              queryset=PageGalleryFormset.model.objects.filter(page_id=int(pk))
                                              if pk.isdigit() else PageGalleryFormset.model.objects.none()),
                'required_size': PageGalleryFormset.model.required_size,
            },
            'seo': {
                'form': SEOForm(request.POST or None,
                                instance=get_object_or_404(SEOForm.Meta.model, page_id=int(pk))
                                if pk.isdigit() and SEOForm.Meta.model.objects.filter(page_id=pk).exists() else None,
                                prefix='seo'),
            },
            'currentUrl': request.get_full_path(),
        }

    def get(self, request, pk: str) -> HttpResponse:
        return render(request, 'admin/pages/page_card.html', self.get_context(request, pk))

    def post(self, request, pk: str) -> HttpResponse:
        context = self.get_context(request, pk)
        page, gallery, seo = context['page']['form'], context['gallery']['formset'], context['seo']['form']

        if False not in [page.is_valid(), gallery.is_valid(), seo.is_valid()]:
            page.save()

            for page_image in gallery:
                if page_image.is_valid():
                    page_image = page_image.save(commit=False)
                    page_image.page = page.instance
            gallery.save()

            seo = seo.save(commit=False)
            seo.page = page.instance
            seo.save()

            return redirect('pages')

        return render(request, 'admin/pages/index.html', context)


class ContactsPageCardView(View):
    @staticmethod
    def get_context(request, pk=1) -> dict:
        return {
            'title': 'Карточка страницы контактов',
            'page': {
                'formset': ContactsPageCardFormset(request.POST or None, request.FILES or None, prefix='contacts_page'),
                'required_size': ContactsPageCardFormset.model.required_size,
            },
            'seo': {
                'form': SEOForm(request.POST or None,
                                instance=get_object_or_404(SEOForm.Meta.model, contacts_page_id=pk)
                                if SEOForm.Meta.model.objects.filter(contacts_page_id=pk).exists() else None,
                                prefix='seo'),
            },
            'currentUrl': request.get_full_path(),
        }

    def get(self, request) -> HttpResponse:
        return render(request, 'admin/pages/contacts_page_card.html', self.get_context(request))

    def post(self, request) -> HttpResponse:
        context = self.get_context(request, pk=1)
        page, seo = context['page']['formset'], context['seo']['form']

        if False not in [page.is_valid(), seo.is_valid()]:
            page.save()

            seo = seo.save(commit=False)
            seo.contacts_page = page[0].instance
            seo.save()

            return redirect('pages')

        return render(request, 'admin/pages/index.html', context)


class PageCardDeleteView(View):
    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        model = PageCardForm.Meta.model
        page_to_delete = get_object_or_404(model, pk=pk)
        page_to_delete.delete()
        return redirect('pages')


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
