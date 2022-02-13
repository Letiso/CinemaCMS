from django.db import models
from datetime import date
from django.utils import timezone

# region SEO
class SEO(models.Model):
    url = models.CharField('URL', max_length=256)
    title = models.CharField('Заголовок', max_length=256)
    keywords = models.CharField('Ключевые слова', max_length=256)
    description = models.TextField('Описание', )


# endregion SEO

# region Banners
banners_media_path = 'main/index/banners'


class TopBanner(models.Model):
    image_required_size = (1000, 190)
    image = models.ImageField('Баннер', upload_to=f'{banners_media_path}/top')
    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class BackgroundImage(models.Model):
    image_required_size = (2000, 3000)
    image = models.ImageField('Фоновое изображение', upload_to=f'{banners_media_path}/background')
    is_active = models.BooleanField(default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class NewsBanner(models.Model):
    image_required_size = (1000, 190)
    image = models.ImageField('Баннер', upload_to=f'{banners_media_path}/news')
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
class MovieCard(models.Model):
    title = models.CharField('Название фильма', max_length=256)
    description = models.TextField('Описание')
    release_date = models.DateField('Дата релиза', default=date.today)

    main_image_required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка')

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


class MovieFrame(models.Model):
    card = models.ForeignKey(MovieCard, on_delete=models.CASCADE, related_name='gallery')

    image_required_size = (1000, 190)
    image = models.ImageField('Кадр из фильма')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


# endregion Movies

# region Cinemas
class CinemaCard(models.Model):
    name = models.CharField('Название кинотеатра', max_length=256)
    description = models.TextField('Описание')
    amenities = models.TextField('Условия')

    logo_required_size = (1000, 190)
    logo = models.ImageField('Логотип')

    banner_required_size = (1000, 190)
    banner = models.ImageField('Главная картинка')

    is_active = models.BooleanField('Активен', default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='cinema', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'logo': cls.logo_required_size, 'banner': cls.banner_required_size}


class CinemaGallery(models.Model):
    card = models.ForeignKey(CinemaCard, on_delete=models.CASCADE, related_name='gallery')
    image_required_size = (1000, 190)
    image = models.ImageField('Фото кинотеатра')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


class CinemaHallCard(models.Model):
    cinema = models.ForeignKey(CinemaCard, on_delete=models.CASCADE, related_name='halls')
    number = models.CharField('Номер зала', max_length=256)
    description = models.TextField('Описание зала')

    scheme_required_size = (1000, 190)
    scheme = models.ImageField('Схема зала')

    banner_required_size = (1000, 190)
    banner = models.ImageField('Баннер')

    is_active = models.BooleanField('Активен', default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='hall', null=True)

    @classmethod
    def get_required_sizes(cls):
        return {'scheme': cls.scheme_required_size, 'banner': cls.banner_required_size}


class CinemaHallGallery(models.Model):
    card = models.ForeignKey(CinemaHallCard, on_delete=models.CASCADE, related_name='gallery')
    image_required_size = (1000, 190)
    image = models.ImageField('Фото зала')

    is_active = models.BooleanField('Активен', default=False)

    @classmethod
    def get_required_sizes(cls):
        return {'image': cls.image_required_size}


# endregion Cinemas

# region MovieSessions
class MovieSession(models.Model):
    movie = models.OneToOneField(MovieCard, on_delete=models.CASCADE, related_name='movie_session')
    hall = models.OneToOneField(CinemaHallCard, on_delete=models.CASCADE, related_name='movie_session')
    start_date_time = models.DateTimeField(default=timezone.now)

    required_size = (1000, 190)
    image = models.ImageField('Кадр из фильма')
    is_active = models.BooleanField('Активен', default=False)


# endregion MovieSessions

# region News
class NewsCard(models.Model):
    title = models.CharField('Название новости', max_length=256)
    publication_date = models.DateField('Дата публикации', default=date.today)
    description = models.TextField('Описание')
    required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка')
    video_link = models.CharField('Ссылка на видео', max_length=256)

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='news', null=True)


class NewsGallery(models.Model):
    card = models.ForeignKey(NewsCard, on_delete=models.CASCADE, related_name='gallery')
    required_size = (1000, 190)
    image = models.ImageField('Картинка к новости')
    is_active = models.BooleanField('Активен', default=False)


# endregion News

# region Promotion
class PromotionCard(models.Model):
    title = models.CharField('Название акции', max_length=256)
    publication_date = models.DateField('Дата публикации', default=date.today)
    description = models.TextField('Описание')
    required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка')
    video_link = models.CharField('Ссылка на видео', max_length=256)

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='promotion', null=True)


class PromotionGallery(models.Model):
    card = models.ForeignKey(PromotionCard, on_delete=models.CASCADE, related_name='gallery')
    required_size = (1000, 190)
    image = models.ImageField('Картинка к акции')
    is_active = models.BooleanField('Активен', default=False)


# endregion Promotion

# region Pages
class MainPageCard(models.Model):
    title = models.CharField('Название страницы', max_length=256)
    phone = models.CharField('Телефон', max_length=256)
    seo_text = models.TextField('SEO текст')

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='main_page', null=True)


class PageCard(models.Model):
    title = models.CharField('Название страницы', max_length=256)
    description = models.TextField('Описание')
    required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка')

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='page', null=True)


class PageGallery(models.Model):
    card = models.ForeignKey(PageCard, on_delete=models.CASCADE, related_name='gallery')
    required_size = (1000, 190)
    image = models.ImageField('Картинка к акции')

    is_active = models.BooleanField('Активен', default=False)


class ContactsPageCard(models.Model):
    title = models.CharField('Название кинотеатра', max_length=256)
    address = models.TextField('Адрес')
    map_coordinates = models.CharField('Координаты для карты', max_length=256)
    required_size = (1000, 190)
    main_image = models.ImageField('Лого')

    is_active = models.BooleanField('Активен', default=False)
    date_created = models.DateTimeField(default=timezone.now)
    seo = models.OneToOneField(SEO, on_delete=models.CASCADE, related_name='contacts_page', null=True)


# endregion Pages

# region Mailing
class EmailMailingHTMLMessage(models.Model):
    """History of 5 last used html-messages for e-mail mailing"""
    name = models.CharField(max_length=256, default='')
    message = models.FileField('Загрузить HTML-письмо', upload_to='admin/mailing/last-html-messages', blank=True)


# endregion Mailing
