import datetime
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


class ColorsListGenerator:
    cycle_counter = -1
    COLORS = [
        {"name": "dark", "rgba": "rgba(52, 58, 64, 0.9)", "hex": "#343a40"},
        {"name": "primary", "rgba": "rgba(0, 123, 255, 0.9)", "hex": "#007bff"},
        {"name": "secondary", "rgba": "rgba(108, 117, 125, 0.9)", "hex": "#6c757d"},
        {"name": "danger", "rgba": "rgba(220, 53, 69, 0.9)", "hex": "#dc3545"},
        {"name": "success", "rgba": "rgba(40, 167, 69, 0.9)", "hex": "#28a745"},
        {"name": "warning", "rgba": "rgba(255, 193, 75, 0.9)", "hex": "#ffc107"},
        {"name": "info", "rgba": "rgba(23, 162, 184, 0.9)", "hex": "#17a2b8"},
    ]

    @property
    def get_color(self):
        if self.cycle_counter < len(self.COLORS):
            self.cycle_counter += 1
        else:
            self.cycle_counter = -1
        return self.COLORS[self.cycle_counter]

    def __getattr__(self, item):
        if item in ("name", "rgba", "hex"):
            return self.get_color[item]
        else:
            return object.__getattribute__(self, item)


# region Mixins
class CustomAbstractView(View):
    template_name: str = None
    context: dict = None

    @staticmethod
    def get_context(*args, **kwargs) -> dict:
        return {'required_sizes': {}}

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.context = self.get_context(request, *args, **kwargs)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name, self.context)


class CardView(CustomAbstractView):
    success_url = request = None
    contains_gallery: bool = True

    card_prefix = card_model = card_form = None
    card_instance = None

    gallery_prefix = gallery_model = gallery_formset = None
    gallery_queryset = None

    seo_instance = None

    def get_card_context(self, pk):
        if pk:
            self.card_instance = get_object_or_404(self.card_model, pk=pk)

        request_data = self.request.POST or None, self.request.FILES or None
        form = self.card_form(*request_data, instance=self.card_instance, prefix=self.card_prefix)

        self.context['required_sizes'][self.card_prefix] = self.card_model.get_required_sizes()

        return {'form': form}

    def get_gallery_context(self, pk):
        self.gallery_queryset = self.gallery_model.objects.filter(card_id=pk) \
            if pk else self.gallery_model.objects.none()

        request_data = self.request.POST or None, self.request.FILES or None
        formset = self.gallery_formset(*request_data, queryset=self.gallery_queryset, prefix=self.gallery_prefix)

        self.context['required_sizes'][self.gallery_prefix] = self.gallery_model.get_required_sizes()

        return {'formset': formset}

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

        self.context['required_sizes'] = json.dumps(self.context['required_sizes'])

        return self.context

    def get_forms_to_save(self) -> tuple:
        forms_to_save = (
            self.context['card']['form'],
            self.context['seo']['form'],

            self.context['gallery']['formset'] if self.contains_gallery else None
        )  # getting tuple of form/formset objects

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

        return super().post(request, *args, **kwargs)


class CardDeleteView(View):
    model = success_url = None

    def get(self, request, pk) -> HttpResponseRedirect:
        card_to_delete = get_object_or_404(self.model, pk=pk)
        card_to_delete.delete()

        return redirect(self.success_url)


# endregion Mixins

# region Statistics
class StatisticsView(CustomAbstractView):
    template_name = 'admin/statistics.html'

    def set_users_context(self):
        user_model = get_user_model().objects
        self.context['users'] = user_model.order_by('date_joined')

        active_users_range = timezone.now() - datetime.timedelta(days=31)
        self.context['active_users'] = user_model.filter(last_login__gte=active_users_range
                                                         ).order_by('last_login')
        self.context['users_gender'] = [user_model.filter(gender='m'), user_model.filter(gender='f')]

    def set_months_movie_sessions_context(self):
        half_year_ago = timezone.now() - datetime.timedelta(days=180)
        movie_sessions = MovieSession.objects.filter(start_datetime__gte=half_year_ago)

        # set months labels
        now = timezone.now()
        year, month = now.year, now.month

        months_datetime_list = [
            datetime.date(year=year,
                          month=month if month > 0 else 12 + month,
                          day=1)
            for month in range(month - 5, month + 1)
        ]
        self.context["movie_sessions_per_month"] = {"month_labels": months_datetime_list}

        # set months data
        movie_types = MovieCard.get_every_movie_type_tuple()
        get_color = ColorsListGenerator()

        total_movie_sessions_count = []
        # на каждый тип кино
        for movie_type in movie_types:
            movie_sessions_count = []
            # на каждый месяц
            for month in months_datetime_list:
                counter = 0
                # количество сеансов
                for movie_session in movie_sessions:
                    session_month = movie_session.start_datetime.month == month.month
                    session_type = movie_session.movie_type == movie_type

                    if session_month and session_type:
                        counter += 1
                movie_sessions_count.append(counter)
            total_movie_sessions_count.append(
                (movie_type, get_color.rgba, json.dumps(movie_sessions_count), )
            )
        self.context["movie_sessions_per_month"]["sessions_count"] = total_movie_sessions_count

    def set_month_tickets_sell_context(self):
        month_ago = timezone.now() - datetime.timedelta(days=30)
        movie_sessions = MovieSession.objects.filter(start_datetime__gt=month_ago)

    def get_context(self, request) -> dict:
        self.context = super().get_context()

        self.set_users_context()
        self.set_months_movie_sessions_context()
        self.set_month_tickets_sell_context()

        # self.context[""]
        return self.context


# endregion Statistics

# region Banners
class BannersView(CustomAbstractView):
    template_name = 'admin/banners/index.html'
    request = None

    def get_top_banners_context(self) -> dict:
        prefix = 'top_banners'

        request_data = self.request.POST or None, self.request.FILES or None
        formset = TopBannerFormSet(*request_data, prefix=prefix)

        carousel_instance = BannersCarousel.objects.get_or_create(pk=1)[0]
        carousel = BannersCarouselForm(*request_data, instance=carousel_instance, prefix=prefix)

        self.context['required_sizes'][prefix] = TopBanner.get_required_sizes()

        return {'formset': formset, 'carousel': carousel}

    def get_background_image_context(self) -> dict:
        prefix = 'background_image'

        request_data = self.request.POST or None, self.request.FILES or None
        form_instance = BackgroundImage.objects.get_or_create(pk=1)[0]
        form = BackgroundImageForm(*request_data, instance=form_instance, prefix=prefix)

        self.context['required_sizes'][prefix] = BackgroundImage.get_required_sizes()

        return {'form': form}

    def get_news_banners_context(self) -> dict:
        prefix = 'news_banners'

        request_data = self.request.POST or None, self.request.FILES or None
        formset = NewsBannerFormSet(*request_data, prefix=prefix)

        carousel_instance = BannersCarousel.objects.get_or_create(pk=2)[0]
        carousel = BannersCarouselForm(*request_data, instance=carousel_instance, prefix=prefix)

        self.context['required_sizes'][prefix] = NewsBanner.get_required_sizes()

        return {'formset': formset, 'carousel': carousel}

    def get_context(self, request) -> dict:
        self.request = request
        self.context = super().get_context()

        self.context['top_banners'] = self.get_top_banners_context()
        self.context['background_image'] = self.get_background_image_context()
        self.context['news_banners'] = self.get_news_banners_context()

        self.context['required_sizes'] = json.dumps(self.context['required_sizes'])

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

        forms_to_save = self.get_forms_to_save()  # getting tuple of form/formset objects
        is_valid = [form.is_valid() for form in forms_to_save]

        if all(is_valid):
            for form in forms_to_save:
                form.save()
            return redirect('admin:banners')

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
    success_url = 'admin:movies'

    card_prefix = 'movie'
    card_model = MovieCard
    card_form = MovieCardForm

    gallery_prefix = 'movie_frame'
    gallery_model = MovieFrame
    gallery_formset = MovieFrameFormset


class MovieCardDeleteView(CardDeleteView):
    model = MovieCard
    success_url = 'admin:movies'


# endregion Movies

# region Cinemas
class CinemasView(CustomAbstractView):
    template_name = 'admin/cinemas/index.html'

    def get_context(self, *kwargs):
        self.context = super().get_context()

        self.context['cinemas'] = CinemaCard.objects.all()
        self.context['halls'] = CinemaHallCard.objects.all()

        return self.context


class CinemaCardView(CardView):
    template_name = 'admin/cinemas/cinema_card.html'
    success_url = 'admin:cinemas'

    card_prefix = 'cinema'
    card_model = CinemaCard
    card_form = CinemaCardForm

    gallery_prefix = 'cinema_image'
    gallery_model = CinemaGallery
    gallery_formset = CinemaGalleryFormset


class CinemaCardDeleteView(CardDeleteView):
    model = CinemaCard
    success_url = 'admin:cinemas'


class CinemaHallCardView(CardView):
    template_name = 'admin/cinemas/hall_card.html'
    success_url = 'admin:cinemas'

    card_prefix = 'hall'
    card_model = CinemaHallCard
    card_form = CinemaHallCardForm

    gallery_prefix = 'hall_image'
    gallery_model = CinemaHallGallery
    gallery_formset = CinemaHallGalleryFormset

    def get_context(self, request, pk, cinema_pk):
        self.context = super().get_context(request, pk)
        self.context['cinema_pk'] = cinema_pk

        return self.context

    def save(self, card, seo, gallery=None) -> bool:
        is_valid = [form.is_valid() for form in (card, seo, gallery) if form]

        if all(is_valid):
            cinema_pk = self.context['cinema_pk']
            cinema_instance = CinemaCard.objects.get(pk=cinema_pk)

            seo.save()

            card = card.save(commit=False)
            card.cinema = cinema_instance
            card.seo = seo.instance
            card.save()

            for image in gallery:
                if image.is_valid():
                    image = image.save(commit=False)
                    image.card = card
            gallery.save()

            return True


class CinemaHallCardDeleteView(CardDeleteView):
    model = CinemaHallCard
    success_url = 'admin:cinemas'


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
    success_url = 'admin:news'

    card_prefix = 'news'
    card_model = NewsCard
    card_form = NewsCardForm

    gallery_prefix = 'news_image'
    gallery_model = NewsGallery
    gallery_formset = NewsGalleryFormset


class NewsCardDeleteView(CardDeleteView):
    model = NewsCard
    success_url = 'admin:news'


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
    success_url = 'admin:promotion'

    card_prefix = 'promotion'
    card_model = PromotionCard
    card_form = PromotionCardForm

    gallery_prefix = 'promotion_image'
    gallery_model = PromotionGallery
    gallery_formset = PromotionGalleryFormset


class PromotionCardDeleteView(CardDeleteView):
    model = PromotionCard
    success_url = 'admin:promotion'


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
    def get_about_the_cinema_page_context():
        about_the_cinema_page_card = AboutTheCinemaPageCard.objects.filter(pk=1).first()
        if not about_the_cinema_page_card:
            about_the_cinema_page_card = AboutTheCinemaPageCard.objects.create(pk=1, title='О кинотеатре')

        return about_the_cinema_page_card

    @staticmethod
    def get_primary_pages_context():
        titles = (
            'Кафе - Бар', 'VIP - зал', 'Детская комната', 'Реклама'
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
        self.context['about_the_cinema_page'] = self.get_about_the_cinema_page_context()
        self.context['primary_page_list'] = self.get_primary_pages_context()
        self.context['custom_page_list'] = self.get_custom_pages_context()
        self.context['contacts_page'] = self.get_contacts_page_context()

        return self.context


class MainPageCardView(CardView):
    template_name = 'admin/pages/main_page_card.html'
    success_url = 'admin:pages'
    contains_gallery = False

    card_prefix = 'main_page'

    def get_card_context(self, pk):
        self.card_instance = get_object_or_404(MainPageCard, pk=pk)

        form = MainPageCardForm(self.request.POST or None, instance=self.card_instance, prefix=self.card_prefix)

        return {'form': form}

    def get_context(self, request):
        return super().get_context(request, pk='1')


class AboutTheCinemaPageCardView(CardView):
    template_name = 'admin/pages/about_the_cinema_page_card.html'
    success_url = 'admin:pages'
    contains_gallery = False

    card_prefix = 'about_the_cinema_page'
    card_model = AboutTheCinemaPageCard
    card_form = AboutTheCinemaPageCardForm

    def get_context(self, request):
        self.context = super().get_context(request, pk='1')

        return self.context


class PageCardView(CardView):
    template_name = 'admin/pages/page_card.html'
    success_url = 'admin:pages'

    card_prefix = 'page'
    card_model = PageCard
    card_form = PageCardForm

    gallery_prefix = 'page_image'
    gallery_model = PageGallery
    gallery_formset = PageGalleryFormset


class PageCardDeleteView(CardDeleteView):
    model = PageCard
    success_url = 'admin:pages'


class ContactsPageCardView(CardView):
    template_name = 'admin/pages/contacts_page_card.html'
    success_url = 'admin:pages'
    contains_gallery = False

    card_prefix = 'contacts_page'

    def get_card_context(self, *args):
        request_data = self.request.POST or None, self.request.FILES or None
        formset = ContactsPageCardFormset(*request_data, prefix=self.card_prefix)

        self.context['required_sizes'][self.card_prefix] = ContactsPageCard.get_required_sizes()

        return {'formset': formset}

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


# endregion Pages

# region User
class UsersListView(CustomAbstractView):
    template_name = 'admin/users/index.html'

    def get_context(self, request) -> dict:
        self.context = super().get_context()
        self.context['users'] = get_user_model().objects.order_by('date_joined')

        return self.context


class UserUpdateView(UpdateView):
    model = get_user_model()
    template_name = 'admin/users/update_user.html'
    success_url = 'admin:users'

    form_class = ExtendedUserUpdateForm

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        chosen_user = context['form'].instance
        context['chosen_user'] = chosen_user

        return context


class UserDeleteView(CardDeleteView):
    model = get_user_model()
    success_url = 'admin:users'


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
            return redirect('admin:mailing')

        return super().post(request)

# endregion Mailing
