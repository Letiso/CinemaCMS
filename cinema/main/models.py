from django.db import models
from datetime import date

# region Banners
banners_media_path = 'main/index/banners'


class TopBanner(models.Model):
    required_size = (1000, 190)
    image = models.ImageField('Баннер', upload_to=f'{banners_media_path}/top')
    is_active = models.BooleanField('Активен', default=False)
    objects = models.Manager()


class BackgroundImage(models.Model):
    required_size = (2000, 3000)
    image = models.ImageField('Фоновое изображение', upload_to=f'{banners_media_path}/background')
    is_active = models.BooleanField(default=False)

    objects = models.Manager()


class NewsBanner(models.Model):
    required_size = (1000, 190)
    image = models.ImageField('Баннер', upload_to=f'{banners_media_path}/news')
    is_active = models.BooleanField('Активен', default=False)

    objects = models.Manager()


class BannersCarousel(models.Model):
    TIME = tuple(
        (f'{second}000', f'{second} с') for second in range(1, 10)
    )

    name = models.CharField(max_length=128, unique=True)
    data_interval = models.CharField('Скорость вращения', max_length=4, choices=TIME, default='5000')
    is_active = models.BooleanField(default=False)

    objects = models.Manager()


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
    seo = models.OneToOneField('SEO', on_delete=models.CASCADE, related_name='page', default=None)

    objects = models.Manager()


class MovieFrame(models.Model):
    movie = models.ForeignKey(MovieCard, on_delete=models.CASCADE, related_name='gallery')
    required_size = (1000, 190)
    image = models.ImageField()
    is_active = models.BooleanField()

    objects = models.Manager()


# endregion Movies

# region SEO
class SEO(models.Model):
    url = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    keywords = models.CharField(max_length=256)
    description = models.TextField()


# endregion SEO
