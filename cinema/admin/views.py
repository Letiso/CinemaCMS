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
    template_name:str = None
    context:dict = None

    @staticmethod
    def get_context(*args, **kwargs) -> dict:
        return {}

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.context = self.get_context(request, *args, **kwargs)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name, self.context)


class CardView(CustomAbstractView):
    success_url = request = None
    contains_gallery:bool = True

    card_prefix = card_model = card_form = None
    card_instance = None

    gallery_prefix = gallery_model = gallery_formset = None
    gallery_queryset = None

    seo_instance = None

    def get_card_context(self, pk):
        required_size = self.card_model.required_size
        if pk:
            self.card_instance = get_object_or_404(self.card_model, pk=pk)

        request_data = self.request.POST or None, self.request.FILES or None
        form = self.card_form(*request_data, instance=self.card_instance, prefix=self.card_prefix)

        return {'required_size': required_size, 'form': form}

    def get_gallery_context(self, pk):
        required_size = self.gallery_model.required_size

        self.gallery_queryset = self.gallery_model.objects.filter(card_id=pk) \
                     if pk else self.gallery_model.objects.none()

        request_data = self.request.POST or None, self.request.FILES or None
        formset = self.gallery_formset(*request_data, queryset=self.gallery_queryset, prefix=self.gallery_prefix)

        return {'required_size': required_size, 'formset': formset}

    def get_seo_context(self, pk):
        if pk:
            related_name_and_pk = {self.card_prefix: pk}
            # get something looks like  * movie_card=pk *  as a result

            instance = SEO.objects.filter(**related_name_and_pk).first()
            if instance:
                self.seo_instance = instance

        form = SEOForm(self.request.POST or None, instance=self.seo_instance, prefix='seo')

        return {'form': form}

    def get_context(self, request, pk):
        self.request = request
        pk = int(pk) if pk.isdigit() else None
        # For cases when we create a new card,
        # pk at url have value "new" instead of numeric value
        self.context = super().get_context()

        self.context['pk'] = pk
        self.context['card'] = self.get_card_context(pk)
        if self.contains_gallery:
            self.context['gallery'] = self.get_gallery_context(pk)
        self.context['seo'] = self.get_seo_context(pk)
        self.context['currentUrl'] = request.get_full_path()

        return self.context

    def get_forms_to_save(self) -> tuple:
        forms_to_save = (
            self.context['card']['form'],
            self.context['seo']['form'],

            self.context['gallery']['formset'] if self.contains_gallery else None
        ) # getting tuple of form/formset objects

        return forms_to_save

    @staticmethod
    def save(card, seo, gallery=None) -> bool:
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
        self.context = self.get_context(request, *args, **kwargs)

        forms_to_save = self.get_forms_to_save()
        if self.save(*forms_to_save):
            return redirect(self.success_url)

        return super().post(request, pk, *args, **kwargs)


# endregion Mixins

# region Statistics
class StatisticsView(CustomAbstractView):
    template_name = 'admin/statistics.html'


# endregion Statistics

# region Banners
class BannersView(CustomAbstractView):
    template_name = 'admin/banners/index.html'
    request = None

    def get_top_banners_context(self) -> dict:
        prefix = 'top_banners'

        required_size = TopBanner.required_size

        request_data = self.request.POST or None, self.request.FILES or None
        formset = TopBannerFormSet(*request_data, prefix=prefix)

        carousel_instance = BannersCarousel.objects.get_or_create(pk=1)[0]
        carousel = BannersCarouselForm(*request_data, instance=carousel_instance, prefix=prefix)

        return {'required_size': required_size, 'formset': formset, 'carousel': carousel}

    def get_background_image_context(self) -> dict:
        prefix = 'background_image'

        required_size =  BackgroundImage.required_size

        request_data = self.request.POST or None, self.request.FILES or None
        form_instance = BackgroundImage.objects.get_or_create(pk=1)[0]
        form = BackgroundImageForm(*request_data, instance=form_instance, prefix=prefix)

        return {'required_size': required_size, 'form': form}

    def get_news_banners_context(self) -> dict:
        prefix = 'news_banners'

        required_size = NewsBanner.required_size

        request_data = self.request.POST or None, self.request.FILES or None
        formset = NewsBannerFormSet(*request_data, prefix=prefix)

        carousel_instance = BannersCarousel.objects.get_or_create(pk=2)[0]
        carousel = BannersCarouselForm(*request_data, instance=carousel_instance, prefix=prefix)

        return {'required_size': required_size, 'formset': formset, 'carousel': carousel}

    def get_context(self, request) -> dict:
        self.request = request
        self.context = super().get_context()

        self.context['top_banners'] = self.get_top_banners_context()
        self.context['background_image'] = self.get_background_image_context()
        self.context['news_banners'] = self.get_news_banners_context()

        return self.context

    def get_forms_to_save(self):
        # In cases when we have several submits at one page
        # we have to know which was the pressed
        forms_to_save = {
            'top_banners': (
                self.context['top_banners']['formset'],
                self.context['top_banners']['carousel']
            ),
            'background_image': (
                self.context['background_image']['form'],
            ),
            'news_banners': (
                self.context['news_banners']['formset'],
                self.context['news_banners']['carousel']
            ),
        }

        for prefix in forms_to_save:
            # It's looking for submit name
            if prefix in self.request.POST.keys():
                return forms_to_save[prefix]

    def post(self, request) -> HttpResponse:
        self.context = self.get_context(request)

        forms_to_save = self.get_forms_to_save() # getting tuple of form/formset objects
        is_valid = [form.is_valid() for form in forms_to_save]

        if all(is_valid):
            for form in forms_to_save:
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
            main_page_card = MainPageCard.objects.create(subject_id=1, title='Главная страница')

        return main_page_card

    @staticmethod
    def get_primary_pages_context():
        titles = (
            'О кинотеатре', 'Кафе - Бар', 'VIP - зал', 'Реклама', 'Детская комната'
        )

        pk_range = 1, len(titles) + 1
        primary_pages = [
            PageCard.objects.get_or_create(pk=pk)[0] for pk in range(*pk_range)
        ]

        for page_card in primary_pages:
            if not page_card.title:
                page_card.title = titles[page_card.pk - 1]
                page_card.save()

        return primary_pages

    def get_custom_pages_context(self):
        primary_pages_count = len(self.context['primary_page_list']) + 1
        not_custom_pages_id = list(range(1, primary_pages_count))
        # exclude *primary_page_list* from queryset by creating [1, 2, 3, ...]

        custom_pages = PageCard.objects.exclude(id__in=not_custom_pages_id)

        return custom_pages

    @staticmethod
    def get_contacts_page_context():
        contacts_page_card = ContactsPageCard.objects.filter(pk=1).first()
        if not contacts_page_card:
            contacts_page_card = ContactsPageCard.objects.create(subject_id=1, title='Контакты')

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

        form = MainPageCardForm(self.request.POST or None, instance=self.card_instance, prefix=self.card_prefix)

        return {'form': form}

    def get_context(self, request):
        return super().get_context(request, pk='1')


class PageCardView(CardView):
    template_name = 'admin/pages/page_card.html'
    success_url = 'pages'

    card_prefix = 'page'
    card_model = PageCard
    card_form = PageCardForm

    gallery_prefix = 'page_image'
    gallery_model = PageGallery
    gallery_formset = PageGalleryFormset


class ContactsPageCardView(CardView):
    template_name = 'admin/pages/contacts_page_card.html'
    success_url = 'pages'
    contains_gallery = False

    card_prefix = 'contacts_page'

    def get_card_context(self, *args):
        required_size = ContactsPageCard.required_size

        request_data = self.request.POST or None, self.request.FILES or None
        formset = ContactsPageCardFormset(*request_data, prefix=self.card_prefix)

        return {'required_size': required_size, 'formset': formset}

    def get_context(self, request):
        return super().get_context(request, pk='1')

    def get_forms_to_save(self):
        forms_to_save = (
            self.context['card']['formset'],
            self.context['seo']['form']
        )

        return forms_to_save

    def save(self, card, seo) -> bool:
        is_valid = [card.is_valid(), seo.is_valid()]
        if all(is_valid):
            seo.save()

            first_contacts_block = card[0].save(commit=False)
            first_contacts_block.seo = seo.instance
            first_contacts_block.save()
            card.save()

            return True


class PageCardDeleteView(View):
    @staticmethod
    def get(request, pk) -> HttpResponseRedirect:
        model = PageCard
        page_card_to_delete = get_object_or_404(model, pk=pk)
        page_card_to_delete.delete()

        return redirect('pages')


# endregion Pages

# region User
class UsersListView(CustomAbstractView):
    template_name = 'admin/users/index.html'

    def get_context(self, request) -> dict:
        self.context = super().get_context()
        self.context['users'] = get_user_model().objects.all()

        return self.context


class UserUpdateView(CustomAbstractView):
    template_name = 'admin/users/update_password.html'

    def get_context(self, request, pk) -> dict:
        self.context = super().get_context()

        chosen_user = get_user_model().objects.get(pk=pk)
        self.context['chosen_user'] = chosen_user
        self.context['form'] = ExtendedUserUpdateForm(instance=chosen_user)

        return self.context


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

    def get_context(self, request) -> dict:
        self.context = super().get_context()

        self.context['users'] = get_user_model().objects.all()
        self.context['SMS'] = SendSMSForm(request.POST or None, prefix='SMS')
        self.context['email'] = SendEmailForm(request.POST or None, request.FILES or None, prefix='email')
        self.context['last_html_messages'] = EmailMailingHTMLMessage.objects.all()

        return self.context

    def get_mailing_form(self, request):
        # In cases when we have several submits at one page
        # we have to know which was the pressed
        mailing_forms = {
            'SMS': self.context['SMS'],
            'email': self.context['email']
        }

        for prefix in mailing_forms:
            # It's looking for submit name
            if prefix in request.POST.keys():
                return mailing_forms[prefix]

    @staticmethod
    def start_mailing(form):
        if form.is_valid():
            send_to_everyone, message, checked_users = (form.cleaned_data['mailing_type'],
                                                        form.cleaned_data['message'],
                                                        form.cleaned_data['checked_users'])
            receivers_filter = {} if send_to_everyone \
                else {'id__in': json.loads(checked_users)}

            send_mail.delay(form.prefix, message, receivers_filter)

            return True

    def post(self, request) -> HttpResponse:
        self.context = self.get_context(request)

        current_form = self.get_mailing_form(request)
        mailing_was_started = self.start_mailing(current_form)
        if mailing_was_started:
            return redirect('mailing')

        return super().post(request)


# endregion Mailing
