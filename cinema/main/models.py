from django.db import models
from datetime import date
from django.utils import timezone


# region Banners
banners_media_path = 'main/index/banners'


class TopBanner(models.Model):
    required_size = (1000, 190)
    image = models.ImageField('Баннер', upload_to=f'{banners_media_path}/top')
    is_active = models.BooleanField('Активен', default=False)


class BackgroundImage(models.Model):
    required_size = (2000, 3000)
    image = models.ImageField('Фоновое изображение', upload_to=f'{banners_media_path}/background')
    is_active = models.BooleanField(default=False)


class NewsBanner(models.Model):
    required_size = (1000, 190)
    image = models.ImageField('Баннер', upload_to=f'{banners_media_path}/news')
    is_active = models.BooleanField('Активен', default=False)


class BannersCarousel(models.Model):
    TIME = tuple(
        (f'{second}000', f'{second} с') for second in range(1, 10)
    )

    name = models.CharField(max_length=128, unique=True)
    data_interval = models.CharField('Скорость вращения', max_length=4, choices=TIME, default='5000')
    is_active = models.BooleanField(default=False)


# endregion Banners

# region Movies
class MovieCard(models.Model):
    TYPES = tuple(
        (movie_type, movie_type) for movie_type in ('2D', '3D', 'IMAX')
    )

    title = models.CharField('Название фильма', max_length=256)
    description = models.TextField('Описание')
    release_date = models.DateField('Дата релиза', default=date.today)
    required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка')
    trailer_link = models.CharField('Ссылка на трейлер', max_length=256)
    movie_type = models.CharField('Тип кино', max_length=10, choices=TYPES)

    is_active = models.BooleanField('Активен', default=False)
    date_created = models.DateTimeField(default=timezone.now)


class MovieFrame(models.Model):
    movie = models.ForeignKey(MovieCard, on_delete=models.CASCADE, related_name='gallery')
    required_size = (1000, 190)
    image = models.ImageField('Кадр из фильма')
    is_active = models.BooleanField('Активен', default=False)


# endregion Movies

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


class NewsGallery(models.Model):
    news = models.ForeignKey(NewsCard, on_delete=models.CASCADE, related_name='gallery')
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


class PromotionGallery(models.Model):
    promotion = models.ForeignKey(PromotionCard, on_delete=models.CASCADE, related_name='gallery')
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


class PageCard(models.Model):
    title = models.CharField('Название страницы', max_length=256)
    description = models.TextField('Описание')
    required_size = (1000, 190)
    main_image = models.ImageField('Главная картинка')

    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)


class PageGallery(models.Model):
    page = models.ForeignKey(PageCard, on_delete=models.CASCADE, related_name='gallery')
    required_size = (1000, 190)
    image = models.ImageField('Картинка к акции')

    is_active = models.BooleanField('Активен', default=False)


class ContactsPageCard(models.Model):
    title = models.CharField('Название кинотеатра', max_length=256)
    map_coordinates = models.TextField('Координаты для карты')
    required_size = (1000, 190)
    image = models.ImageField('Лого')

    is_active = models.BooleanField('Активен', default=False)
    date_created = models.DateTimeField(default=timezone.now)


# endregion Pages

# region SEO
class SEO(models.Model):
    movie = models.OneToOneField(MovieCard, on_delete=models.CASCADE, related_name='seo', null=True)
    news = models.OneToOneField(NewsCard, on_delete=models.CASCADE, related_name='seo', null=True)
    promotion = models.OneToOneField(PromotionCard, on_delete=models.CASCADE, related_name='seo', null=True)

    main_page = models.OneToOneField(MainPageCard, on_delete=models.CASCADE, related_name='seo', null=True)
    page = models.OneToOneField(PageCard, on_delete=models.CASCADE, related_name='seo', null=True)
    contacts_page = models.OneToOneField(ContactsPageCard, on_delete=models.CASCADE, related_name='seo', null=True)

    url = models.CharField('URL', max_length=256)
    title = models.CharField('Заголовок', max_length=256)
    keywords = models.CharField('Ключевые слова', max_length=256)
    description = models.TextField('Описание', )


# endregion SEO
