import json
from abc import abstractmethod

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, View
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Model

from .forms import *
from main.models import *

from datetime import date

from cinema.tasks import send_mail
# from user.tests import create_default_users


# region Mixins
class CustomAbstractView(View):
    template_name = context = None

    @staticmethod
    def get_context(*args, **kwargs) -> dict:
        return {}

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.context = self.get_context(request, *args, **kwargs)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name, self.context)


class SeveralHtmlFormsMixin:
    html_forms = request = current_html_form_prefix = None

    def define_current_html_form(self) -> None:
        for prefix in self.html_forms:
            if prefix in self.request.POST:
                self.current_html_form_prefix = prefix
                break

    def try_to_bound(self, prefix) -> dict:
        form_data = {}
        if prefix == self.current_html_form_prefix:
            form_data['data'] = self.request.POST
            form_data['files'] = self.request.FILES
        return form_data


class CardView(CustomAbstractView):
    success_url = request = None
    contains_gallery = True

    card_prefix = card_model = card_form = None
    card_instance = None

    gallery_prefix = gallery_model = gallery_formset = None
    gallery_queryset = None

    seo_instance = None

    def get_card_context(self, pk):
        required_size = self.card_model.required_size
        if pk:
            self.card_instance = get_object_or_404(self.card_model, pk=pk)

        form_data = {
            'data': self.request.POST or None,
            'files': self.request.FILES or None
        }
        form = self.card_form(**form_data, instance=self.card_instance, prefix=self.card_prefix)

        return {'required_size': required_size, 'form': form}

    def get_gallery_context(self, pk):
        required_size = self.gallery_model.required_size

        self.gallery_queryset = self.gallery_model.objects.filter(card_id=pk) \
                     if pk else self.gallery_model.objects.none()

        formset_data = {'data': self.request.POST or None,
                        'files': self.request.FILES or None}
        formset = self.gallery_formset(**formset_data, queryset=self.gallery_queryset, prefix=self.gallery_prefix)

        return {'required_size': required_size, 'formset': formset}

    def get_seo_context(self, pk):
        if pk:
            related_name = {f'{self.context["card"]["form"].prefix}': pk}

            self.seo_instance = get_object_or_404(SEO, **related_name)

        form_data = {'data': self.request.POST or None}
        form = SEOForm(**form_data, instance=self.seo_instance, prefix='seo')

        return {'form': form}

    def get_context(self, request, pk):
        self.request = request
        pk = int(pk) if pk.isdigit() else None
        self.context = super().get_context()

        self.context['pk'] = pk
        self.context['card'] = self.get_card_context(pk)
        if self.contains_gallery:
            self.context['gallery'] = self.get_gallery_context(pk)
        self.context['seo'] = self.get_seo_context(pk)
        self.context['currentUrl'] = request.get_full_path()

        return self.context

    @staticmethod
    def save(card, seo, gallery=None):
        is_valid = [form.is_valid() for form in (card, seo, gallery) if form]

        if all(is_valid):
            seo.save()

            card = card.save(commit=False)
            card.seo = seo.instance
            card.save()

            if gallery:
                for image in gallery:
                    if image.is_valid():
                        image = image.save(commit=False)
                        image.card = card
                gallery.save()

            return True

    def post(self, request, *args, **kwargs) -> HttpResponse:
        context = self.context = self.get_context(request, *args, **kwargs)

        forms_to_save = (
            context['card']['form'], context['seo']['form'],

            context['gallery']['formset'] if self.contains_gallery else None
        ) # getting tuple of form/formset objects

        if self.save(*forms_to_save):
            return redirect(self.success_url)

        return super().post(request, pk, *args, **kwargs)


# endregion Mixins

# region Statistics
class StatisticsView(CustomAbstractView):
    template_name = 'admin/statistics.html'


# endregion Statistics

# region Banners
class BannersView(SeveralHtmlFormsMixin, CustomAbstractView):
    template_name = 'admin/banners/index.html'

    html_forms = {
        'top_banners': lambda self: (
            self.context['top_banners']['formset'], self.context['top_banners']['carousel']
        ),
        'background_image': lambda self: (
            self.context['background_image']['form'],
        ),
        'news_banners': lambda self: (
            self.context['news_banners']['formset'], self.context['news_banners']['carousel']
        ),
    }

    def get_top_banners_context(self) -> dict:
        prefix = 'top_banners'

        required_size = TopBanner.required_size
        formset = TopBannerFormSet(**self.try_to_bound(prefix), prefix=prefix)

        carousel_instance = BannersCarousel.objects.get_or_create(pk=1)[0]
        carousel = BannersCarouselForm(**self.try_to_bound(prefix), instance=carousel_instance, prefix=prefix)

        return {'required_size': required_size, 'formset': formset, 'carousel': carousel}

    def get_background_image_context(self) -> dict:
        prefix = 'background_image'

        required_size =  BackgroundImage.required_size
        form_instance = BackgroundImage.objects.get_or_create(pk=1)[0]
        form = BackgroundImageForm(**self.try_to_bound(prefix), instance=form_instance, prefix=prefix)

        return {'required_size': required_size, 'form': form}

    def get_news_banners_context(self) -> dict:
        prefix = 'news_banners'

        required_size = NewsBanner.required_size
        formset = NewsBannerFormSet(**self.try_to_bound(prefix), prefix=prefix)

        carousel_instance = BannersCarousel.objects.get_or_create(pk=2)[0]
        carousel = BannersCarouselForm(**self.try_to_bound(prefix), instance=carousel_instance, prefix=prefix)

        return {'required_size': required_size, 'formset': formset, 'carousel': carousel}

    def get_context(self, request) -> dict:
        self.request = request
        self.define_current_html_form()
        self.context = super().get_context()

        self.context['top_banners'] = self.get_top_banners_context()
        self.context['background_image'] = self.get_background_image_context()
        self.context['news_banners'] = self.get_news_banners_context()

        return self.context

    def post(self, request) -> HttpResponse:
        self.context = self.get_context(request)

        current_html_form = self.html_forms[self.current_html_form_prefix](self) # getting tuple of form/formset objects
        is_valid = [form.is_valid() for form in current_html_form]

        if all(is_valid):
            for form in current_html_form:
                form.save()
            return HttpResponseRedirect('banners')

        return super().post(request)


# endregion Banners

# region Movies
class MoviesView(CustomAbstractView):
    template_name = 'admin/movies/index.html'

    order = '-date_created'

    def get_context(self, *args):
        self.context = super().get_context()
        today = date.today()

        released_movies = MovieCard.objects.filter(is_active=True, release_date__lte=today)
        self.context['releases'] = released_movies.order_by(self.order)

        announced_movies = MovieCard.objects.filter(is_active=True, release_date__gt=today)
        self.context['announcements'] = announced_movies.order_by(self.order)

        inactive_movies_cards = MovieCard.objects.exclude(is_active=True)
        self.context['inactive_cards'] = inactive_movies_cards.order_by(self.order)

        return self.context


class MovieCardView(CardView):
    template_name = 'admin/movies/movie_card.html'
    success_url = 'movies'

    card_prefix = 'movie'
    card_model = MovieCard
    card_form = MovieCardForm

    gallery_prefix = 'movie_frame'
    gallery_model = MovieFrame
    gallery_formset = MovieFrameFormset


# endregion Movies

# region Cinemas
class CinemasView(CustomAbstractView):
    template_name = 'admin/cinemas.html'


# endregion Cinemas

# region News
class NewsView(CustomAbstractView):
    template_name = 'admin/news/index.html'

    def get_context(self, request):
        self.context = super().get_context()
        self.context['news_list'] = NewsCard.objects.all()

        return self.context


class NewsCardView(CardView):
    template_name = 'admin/news/news_card.html'
    success_url = 'news_conf'

    card_prefix = 'news'
    card_model = NewsCard
    card_form = NewsCardForm

    gallery_prefix = 'news_image'
    gallery_model = NewsGallery
    gallery_formset = NewsGalleryFormset


class NewsCardDeleteView(View):
    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        news_to_delete = get_object_or_404(NewsCard, pk=pk)
        news_to_delete.delete()
        return redirect('news_conf')


# endregion News

# region Promotion
class PromotionListView(CustomAbstractView):
    template_name = 'admin/promotion/index.html'

    def get_context(self, request):
        self.context = super().get_context()
        self.context['promotion_list'] = PromotionCard.objects.all()

        return self.context

class PromotionCardView(CardView):
    template_name = 'admin/promotion/promotion_card.html'
    success_url = 'promotion_conf'

    card_prefix = 'promotion'
    card_model = PromotionCard
    card_form = PromotionCardForm

    gallery_prefix = 'promotion_image'
    gallery_model = PromotionGallery
    gallery_formset = PromotionGalleryFormset


class PromotionCardDeleteView(View):
    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        promotion_to_delete = get_object_or_404(PromotionCard, pk=pk)
        promotion_to_delete.delete()
        return redirect('promotion_conf')


# endregion Promotion

# region Pages
class PageListView(CustomAbstractView):
    template_name = 'admin/pages/index.html'

    @staticmethod
    def get_main_page_context():
        main_page_card = MainPageCard.objects.filter(pk=1).first()
        if not main_page_card:
            main_page_card = MainPageCard.objects.create(pk=1, title='Главная страница')

        return main_page_card

    @staticmethod
    def get_primary_pages_context():
        titles = (
            'О кинотеатре', 'Кафе - Бар', 'VIP - зал', 'Реклама', 'Детская комната'
        )
        pages_count = len(titles)
        primary_pages = [
            PageCard.objects.get_or_create(pk=pk)[0] for pk in range(pages_count)
        ]

        for page_card in primary_pages:
            if not page_card.title:
                page_card.title = titles[page_card.pk]

        return primary_pages

    def get_custom_pages_context(self):
        primary_pages_count = len(self.context['primary_page_list'])
        not_custom_pages_id = list(range(primary_pages_count))
        # exclude *primary_page_list* from queryset by creating [0, 1, 2, ...]

        custom_pages = PageCard.objects.exclude(id__in=not_custom_pages_id)

        return custom_pages

    @staticmethod
    def get_contacts_page_context():
        contacts_page_card = ContactsPageCard.objects.filter(pk=1).first()
        if not contacts_page_card:
            contacts_page_card = ContactsPageCard.objects.create(pk=1, title='Контакты')

        return contacts_page_card

    def get_context(self, request):
        self.context = super().get_context()

        self.context['main_page'] = self.get_main_page_context()
        self.context['primary_page_list'] = self.get_primary_pages_context()
        self.context['custom_page_list'] = self.get_custom_pages_context()
        self.context['contacts_page'] = self.get_contacts_page_context()

        return self.context

class MainPageCardView(CardView):
    template_name = 'admin/pages/main_page_card.html'
    success_url = 'pages'
    contains_gallery = False

    card_prefix = 'main_page'

    def get_card_context(self, pk):
        self.card_instance = get_object_or_404(MainPageCard, pk=pk)

        form_data = {'data': self.request.POST or None}
        form = MainPageCardForm(**form_data, instance=self.card_instance, prefix=self.card_prefix)

        return {'form': form}

    def get_seo_context(self, pk):
        related_name_and_pk = {f'{self.context["card"]["form"].prefix}': pk}
        # get something looks like  * movie_card=pk *  as a result

        instance = SEO.objects.filter(**related_name_and_pk).first()
        if instance:
            self.seo_instance = instance

        form_data = {'data': self.request.POST or None}
        form = SEOForm(**form_data, instance=self.seo_instance, prefix='seo')

        return {'form': form}

    def get_context(self, request):
        return super().get_context(request, pk='1')


class PageCardView(CardView):
    template_name = 'admin/pages/page_card.html'
    success_url = 'pages'

    context = lambda self, request, pk: {
            'pk': pk,
            'card': {
                'form': PageCardForm(request.POST or None, request.FILES or None,
                                     instance=get_object_or_404(PageCard, pk=int(pk)) if pk.isdigit() else None,
                                     prefix='page'),
                'required_size': PageCard.required_size,
            },
            'gallery': {
                'formset': PageGalleryFormset(request.POST or None, request.FILES or None,
                                              prefix='page_image',
                                              queryset=PageGallery.objects.filter(card_id=int(pk)) if pk.isdigit()
                                              else PageGallery.objects.none()),
                'required_size': PageGallery.required_size,
            },
            'seo': {
                'form': SEOForm(request.POST or None,
                                instance=instance if (instance :=
                                                      SEO.objects.filter(page=pk).first()) else None,
                                prefix='seo'),
            },
            'currentUrl': request.get_full_path(),
        }


class ContactsPageCardView(CustomAbstractView):
    template_name = 'admin/pages/contacts_page_card.html'

    context = lambda self, request, pk=1: {
            'title': 'Карточка страницы контактов',
            'card': {
                'formset': ContactsPageCardFormset(request.POST or None, request.FILES or None, prefix='contacts_page'),
                'required_size': ContactsPageCardFormset.model.required_size,
            },
            'seo': {
                'form': SEOForm(request.POST or None,
                                instance=instance if (instance :=
                                                      SEO.objects.filter(contacts_page=pk).first()) else None,
                                prefix='seo'),
            },
            'currentUrl': request.get_full_path(),
        }

    def post(self, request) -> HttpResponse:
        context = self.context = self.context(request)
        card, seo = context['card']['formset'], context['seo']['form']

        if all([card.is_valid(), seo.is_valid()]):
            seo.save()

            first_contacts_block = card[0].save(commit=False)
            first_contacts_block.seo = seo.instance
            first_contacts_block.save()
            card.save()

            return redirect('pages')

        return super().post(request)


class PageCardDeleteView(View):
    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        model = PageCardForm.Meta.model
        page_to_delete = get_object_or_404(model, pk=pk)
        page_to_delete.delete()
        return redirect('pages')


# endregion Pages

# region User
class UsersView(CustomAbstractView):
    template_name = 'admin/users/users.html'

    context = lambda self, request: {
            'users': get_user_model().objects.all(),
        }


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
class MailingView(CustomAbstractView):
    template_name = 'admin/mailing/mailing.html'

    context = lambda self, request: {
        'forms': {
            'SMS': SendSMSForm(**self.try_to_bound('SMS', request)),
            'email': SendEmailForm(**self.try_to_bound('email', request))
        },
        'users': get_user_model().objects.all(),
        'last_html_messages': EmailMailingHTMLMessage.objects.all(),
    }

    def post(self, request) -> HttpResponse:
        context = self.context = self.context(request)

        for prefix, form in context['forms'].items():
            if prefix in request.POST:
                if form.is_valid():
                    send_to_everyone, message, checked_users = (form.cleaned_data['mailing_type'],
                                                                form.cleaned_data['message'],
                                                                form.cleaned_data['checked_users'])
                    receivers_filter = {} if send_to_everyone else {'id__in': json.loads(checked_users)}
                    send_mail.delay(prefix, message, receivers_filter)

                    return redirect('mailing')
                return super().post(request)


# endregion Mailing
