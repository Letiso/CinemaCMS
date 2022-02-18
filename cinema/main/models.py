from django.db import models
from datetime import date
from django.utils import timezone

from abc import abstractmethod
from typing import Dict, Tuple


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
    title = models.CharField('Заголовок', max_length=256)
    keywords = models.CharField('Ключевые слова', max_length=256)
    description = models.TextField('Описание', )


# endregion SEO

# region Banners
class TopBanner(ImageFieldsValidationMixin, models.Model):
    image_required_size = (1000, 190)
    image = models.ImageField('Баннер', upload_to='main/banners/top_banners')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class BackgroundImage(ImageFieldsValidationMixin, models.Model):
    image_required_size = (2000, 3000)
    image = models.ImageField('Фоновое изображение', upload_to='main/banners/background_image')

    is_active = models.BooleanField(default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class NewsBanner(ImageFieldsValidationMixin, models.Model):
    image_required_size = (1000, 190)
    image = models.ImageField('Баннер', upload_to='main/banners/news_banners')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class BannersCarousel(models.Model):
    TIME = tuple(
        (f'{second}000', f'{second} с') for second in range(1, 10)
    )

    data_interval = models.CharField('Скорость вращения', max_length=4, choices=TIME, default='5000')
    is_active = models.BooleanField(default=False)


# endregion Banners

# region Movies
class MovieCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField('Название фильма', max_length=256)
    description = models.TextField('Описание')
    release_date = models.DateField('Дата релиза', default=date.today)

    main_image_required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка', upload_to='main/movies/main_images')

    trailer_link = models.CharField('Ссылка на трейлер', max_length=256)

    two_d = models.BooleanField('2D', default=False)
    three_d = models.BooleanField('3D', default=False)
    imax = models.BooleanField('IMAX', default=False)

    is_active = models.BooleanField('Активен', default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='movie', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'main_image': cls.main_image_required_size}


class MovieFrame(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(MovieCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField('Кадр из фильма', upload_to='main/movies/gallery')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


# endregion Movies

# region Cinemas
class CinemaCard(ImageFieldsValidationMixin, models.Model):
    name = models.CharField('Название кинотеатра', max_length=256)
    description = models.TextField('Описание')
    amenities = models.TextField('Условия')

    logo_required_size = (1000, 190)
    logo = models.ImageField('Логотип', upload_to='main/cinemas/logos')

    banner_required_size = (1000, 190)
    banner = models.ImageField('Главная картинка', upload_to='main/cinemas/banners')

    is_active = models.BooleanField('Активен', default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='cinema', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'logo': cls.logo_required_size, 'banner': cls.banner_required_size}


class CinemaGallery(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(CinemaCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField('Фото кинотеатра', upload_to='main/cinemas/gallery')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class CinemaHallCard(ImageFieldsValidationMixin, models.Model):
    cinema = models.ForeignKey(CinemaCard, on_delete=models.CASCADE, related_name='halls')
    number = models.CharField('Номер зала', max_length=256)
    description = models.TextField('Описание зала')

    scheme_required_size = (1000, 190)
    scheme = models.ImageField('Схема зала', upload_to='main/cinemas/halls/schemes')

    banner_required_size = (1000, 190)
    banner = models.ImageField('Баннер', upload_to='main/cinemas/halls/banners')

    is_active = models.BooleanField('Активен', default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='hall', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'scheme': cls.scheme_required_size, 'banner': cls.banner_required_size}


class CinemaHallGallery(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(CinemaHallCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField('Фото зала', upload_to='main/cinemas/halls/gallery')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


# endregion Cinemas

# region News
class NewsCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField('Название новости', max_length=256)
    publication_date = models.DateField('Дата публикации', default=date.today)
    description = models.TextField('Описание')

    main_image_required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка', upload_to='main/news/main_images')

    video_link = models.CharField('Ссылка на видео', max_length=256)

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='news', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'main_image': cls.main_image_required_size}


class NewsGallery(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(NewsCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField('Картинка к новости', upload_to='main/news/gallery')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


# endregion News

# region Promotion
class PromotionCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField('Название акции', max_length=256)
    publication_date = models.DateField('Дата публикации', default=date.today)
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


class PageCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField('Название страницы', max_length=256)
    description = models.TextField('Описание')

    main_image_required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка', upload_to='main/pages/main_images')

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='page', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'main_image': cls.main_image_required_size}


class PageGallery(ImageFieldsValidationMixin, models.Model):
    card = models.ForeignKey(PageCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField('Картинка к акции', upload_to='main/pages]/gallery')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class ContactsPageCard(ImageFieldsValidationMixin, models.Model):
    title = models.CharField('Название кинотеатра', max_length=256)
    address = models.TextField('Адрес')
    map_coordinates = models.CharField('Координаты для карты', max_length=256)

    main_image_required_size = (1000, 190)
    main_image = models.ImageField('Лого', upload_to='main/pages/main_images')

    is_active = models.BooleanField('Активен', default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='contacts_page', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'main_image': cls.main_image_required_size}


# endregion Pages

# region Mailing
class EmailMailingHTMLMessage(models.Model):
    """History of 5 last used html-messages for e-mail mailing"""
    name = models.CharField(max_length=256, default='')
    message = models.FileField('Загрузить HTML-письмо', upload_to='admin/mailing/last-html-messages', blank=True)


# endregion Mailing
