from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth import get_user_model
import datetime

from abc import abstractmethod
from typing import Dict, Tuple

from cinema.tasks import cancel_ticket_booking


# region Mixins
class ImageFieldsValidationMixin:
    @classmethod
    @abstractmethod
    def get_required_sizes(cls) -> dict: pass

    @classmethod
    def get_image_fields_names(cls):
        return cls.get_required_sizes().keys()


# endregion Mixins

# region SEO
class SEO(models.Model):
    url = models.CharField('URL', max_length=256)
    title = models.CharField(_('Title'), max_length=256)
    keywords = models.CharField(_('Keywords'), max_length=256)
    description = models.TextField(_('Description'), )


# endregion SEO

# region Banners
class TopBanner(ImageFieldsValidationMixin, models.Model):
    image_required_size = (1000, 190)
    image = models.ImageField(_('Banner'), upload_to='main/banners/top_banners')

    is_active = models.BooleanField(_('Is active'), default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class BackgroundImage(ImageFieldsValidationMixin, models.Model):
    image_required_size = (2000, 3000)
    image = models.ImageField(_('Background image'), upload_to='main/banners/background_image')

    is_active = models.BooleanField(default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class NewsBanner(ImageFieldsValidationMixin, models.Model):
    image_required_size = (1000, 190)
    image = models.ImageField(_('Banner'), upload_to='main/banners/news_banners')

    is_active = models.BooleanField(_('Is active'), default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class BannersCarousel(models.Model):

    TIME = (
        (f'{second}000', str(second)) for second in range(1, 10)
    )

    data_interval = models.CharField(_('Rotation speed'), max_length=4, choices=TIME, default='5000')
    is_active = models.BooleanField(default=False)


# endregion Banners

# region Movies
class MovieCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField(_('Movie title'), max_length=256)
    description = models.TextField(_('Description'))
    release_date = models.DateField(_('Release date'), default=timezone.now)

    main_image_required_size = (1000, 190)
    main_image = models.ImageField(_('Poster'), upload_to='main/movies/main_images')

    trailer_link = models.CharField(_('Trailer link'), max_length=256)

    age_rating = models.CharField(_('Age rating'), max_length=2, blank=True)

    two_d = models.BooleanField('2D', default=False)
    three_d = models.BooleanField('3D', default=False)
    imax = models.BooleanField('IMAX', default=False)

    is_active = models.BooleanField(_('Is active'), default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='movie', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'main_image': cls.main_image_required_size}

    @staticmethod
    def get_field_objects(obj):
        field_names = ('two_d', 'three_d', 'imax')
        field_objects = [obj._meta.get_field(field_name) for field_name in field_names]

        return tuple(field_objects)

    @classmethod
    def get_every_movie_type_tuple(cls) -> tuple:
        field_names = [field.verbose_name for field in cls.get_field_objects(cls)]

        return tuple(field_names)

    @property
    def available_movie_types_tuple(self) -> tuple:
        available_fields = [field.verbose_name for field in self.get_field_objects(self)
                            if field.value_from_object(self)]

        return tuple(available_fields)


class MovieFrame(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(MovieCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField(_('Movie frame'), upload_to='main/movies/gallery')

    is_active = models.BooleanField('Is active', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


# endregion Movies

# region Cinemas
class CinemaCard(ImageFieldsValidationMixin, models.Model):
    name = models.CharField(_('Cinema name'), max_length=256)
    description = models.TextField(_('Description'))
    amenities = models.TextField(_('Amenities'))

    logo_required_size = (1000, 190)
    logo = models.ImageField(_('Logo'), upload_to='main/cinemas/logos')

    banner_required_size = (1000, 190)
    banner = models.ImageField(_('Main image'), upload_to='main/cinemas/banners')

    is_active = models.BooleanField(_('Is active'), default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='cinema', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'logo': cls.logo_required_size, 'banner': cls.banner_required_size}


class CinemaGallery(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(CinemaCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField(_('Cinema photo'), upload_to='main/cinemas/gallery')

    is_active = models.BooleanField(_('Is active'), default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class CinemaHallCard(ImageFieldsValidationMixin, models.Model):
    cinema = models.ForeignKey(CinemaCard, on_delete=models.CASCADE, related_name='halls')
    number = models.CharField(_('Hall number'), max_length=256)
    description = models.TextField(_('Hall description'))

    rows_count = models.CharField(_('Rows count'), max_length=3, default=0)
    places_count = models.CharField(_('Places count at row'), max_length=3, default=0)

    banner_required_size = (1000, 190)
    banner = models.ImageField(_('Banner'), upload_to='main/cinemas/halls/banners')

    is_active = models.BooleanField(_('Is active'), default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='hall', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'banner': cls.banner_required_size}


class CinemaHallGallery(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(CinemaHallCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField(_('Hall photo'), upload_to='main/cinemas/halls/gallery')

    is_active = models.BooleanField(_('Is active'), default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


# endregion Cinemas

# region News
class NewsCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField(_('News title'), max_length=256)
    publication_date = models.DateField(_('Publication date'), default=timezone.now)
    description = models.TextField(_('Description'))

    main_image_required_size = (1000, 190)
    main_image = models.ImageField(_('Main image'), upload_to='main/news/main_images')

    video_link = models.CharField(_('Video link'), max_length=256)

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='news', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'main_image': cls.main_image_required_size}


class NewsGallery(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(NewsCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField(_('News image'), upload_to='main/news/gallery')

    is_active = models.BooleanField(_('Is active'), default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


# endregion News

# region Promotion
class PromotionCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField('Название акции', max_length=256)
    publication_date = models.DateField('Дата публикации', default=timezone.now)
    description = models.TextField('Описание')

    main_image_required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка', upload_to='main/promotions/main_images')

    video_link = models.CharField('Ссылка на видео', max_length=256)

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='promotion', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'main_image': cls.main_image_required_size}


class PromotionGallery(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(PromotionCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField('Картинка к акции', upload_to='main/promotions/gallery')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


# endregion Promotion

# region Pages
class MainPageCard(models.Model):
    title = models.CharField('Название страницы', max_length=256)
    first_phone_number = models.CharField('Первый номер телефона', max_length=13, default='')
    second_phone_number = models.CharField('Второй номер телефона', max_length=13, default='')
    seo_text = models.TextField('SEO текст')

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='main_page', null=True)

    def get_phone_numbers(self):
        navbar_phone_numbers = self.first_phone_number, self.second_phone_number

        return navbar_phone_numbers


class AboutTheCinemaPageCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField('Название страницы', max_length=256)
    description = models.TextField('Описание')

    main_image_required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка', upload_to='main/pages/about_the_cinema/')

    description_image_required_size = (1000, 190)
    description_image = models.ImageField('Картинка описания', upload_to='main/pages/about_the_cinema/')

    equipment = models.TextField('Оборудование')

    equipment_image_1_required_size = (1000, 190)
    equipment_image_1 = models.ImageField('Картинка оборудования 1', upload_to='main/pages/about_the_cinema/equipment')

    equipment_image_2_required_size = (1000, 190)
    equipment_image_2 = models.ImageField('Картинка оборудования 2', upload_to='main/pages/about_the_cinema/equipment')

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='about_the_cinema_page', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {
            'main_image': cls.main_image_required_size,
            'description_image': cls.description_image_required_size,
            'equipment_image_1': cls.equipment_image_1_required_size,
            'equipment_image_2': cls.equipment_image_2_required_size,
        }


class PageCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField('Название страницы', max_length=256)
    description = models.TextField('Описание')

    main_image_required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка', upload_to='main/pages/main_images')

    image_1_required_size = (1000, 190)
    image_1 = models.ImageField('Доп. картинка', upload_to='main/pages/additional_images', default='')

    image_2_required_size = (1000, 190)
    image_2 = models.ImageField('Доп. картинка', upload_to='main/pages/additional_images', default='')

    image_3_required_size = (1000, 190)
    image_3 = models.ImageField('Доп. картинка', upload_to='main/pages/additional_images', default='')

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='page', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {
            'main_image': cls.main_image_required_size,
            'image_1': cls.image_1_required_size,
            'image_2': cls.image_2_required_size,
            'image_3': cls.image_3_required_size,
        }


class PageGallery(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(PageCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField('Картинка к странице', upload_to='main/pages/gallery')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class ContactsPageCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField('Название кинотеатра', max_length=256)
    address = models.TextField('Адрес')
    map_coordinates = models.CharField('Координаты для карты', max_length=256)

    logo_required_size = (1000, 190)
    logo = models.ImageField('Лого', upload_to='main/pages/main_images', default='')

    main_image_required_size = (1000, 190)
    main_image = models.ImageField('Фото кинотеатра', upload_to='main/pages/main_images')

    is_active = models.BooleanField('Активен', default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='contacts_page', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {
            'logo': cls.logo_required_size,
            'main_image': cls.main_image_required_size,
        }


# endregion Pages

# region Mailing
class EmailMailingHTMLMessage(models.Model):
    """History of 5 last used html-messages for e-mail mailing"""
    name = models.CharField(max_length=256, default='')
    message = models.FileField('Загрузить HTML-письмо', upload_to='admin/mailing/last-html-messages', blank=True)


# endregion Mailing

# region MovieSessions
class ExtendedManager(models.Manager):
    def bulk_create(self, objs, **kwargs) -> None:
        super().bulk_create(objs, **kwargs)

        for movie_session in objs:
            movie_session.create_tickets()
            cancel_ticket_booking.apply_async(args=[], kwargs={},
                                              eta=movie_session.start_datetime - datetime.timedelta(minutes=30))


class MovieSession(models.Model):
    movie = models.ForeignKey(MovieCard, on_delete=models.DO_NOTHING, related_name='movie_session')
    hall = models.ForeignKey(CinemaHallCard, on_delete=models.DO_NOTHING, related_name='movie_session')

    start_datetime = models.DateTimeField(default=timezone.now)
    movie_type = models.CharField(max_length=10)

    ticket_price = models.CharField(max_length=20, default='1')

    objects = ExtendedManager()

    @classmethod
    def get_movie_sessions_context(cls, **extra_filters) -> tuple:
        time_now = timezone.now()
        coming_time = time_now + datetime.timedelta(days=7)

        movie_sessions = cls.objects.filter(start_datetime__gte=time_now,
                                            start_datetime__lte=coming_time,
                                            **extra_filters).order_by('start_datetime').select_related()

        session_days = [movie_session.start_datetime.date() for movie_session in movie_sessions]
        session_days_unique = sorted(list(set(session_days)))[:7]

        return movie_sessions, session_days_unique

    def create_tickets(self) -> None:
        rows_count = int(self.hall.rows_count)
        rows_range = range(1, rows_count + 1)

        places_count = int(self.hall.places_count)
        places_range = range(1, places_count + 1)

        tickets_to_create = []
        tickets_to_create_data = []

        for row in rows_range:
            for place in places_range:
                tickets_to_create_data.append({'row': row, 'place_number': place})

        for ticket_data in tickets_to_create_data:
            tickets_to_create.append(Ticket(movie_session=self, **ticket_data))

        Ticket.objects.bulk_create(tickets_to_create)


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, related_name='tickets', on_delete=models.DO_NOTHING)

    row = models.IntegerField()
    place_number = models.IntegerField()

    is_sold = models.BooleanField('Продано', default=False)
    is_booked = models.BooleanField('Забронировано', default=False)

    UserModel = get_user_model()
    user = models.ForeignKey(UserModel, related_name='tickets', on_delete=models.DO_NOTHING, blank=True, null=True)


# endregion MovieSessions
