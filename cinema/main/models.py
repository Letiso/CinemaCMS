from django.db import models


# region Banners
banners_path = 'main/index/banners'


class TopBanner(models.Model):
    image = models.ImageField('Баннер', upload_to=f'{banners_path}/top')
    is_active = models.BooleanField('Активен', default=False)
    objects = models.Manager()


class BackgroundImage(models.Model):
    image = models.ImageField('Фоновое изображение', upload_to=f'{banners_path}/background')
    is_active = models.BooleanField('Фоновое изображение', default=False)
    objects = models.Manager()


class NewsBanner(models.Model):
    image = models.ImageField('Баннер', upload_to=f'{banners_path}/news')
    is_active = models.BooleanField('Активен', default=False)
    objects = models.Manager()


class BannersCarousel(models.Model):
    TIME = tuple(
        (f'{second}000', str(second) + ' с') for second in range(1, 10)
    )

    name = models.CharField(max_length=128, unique=True)
    data_interval = models.CharField('Скорость вращения', max_length=4, choices=TIME, default='5000')
    is_active = models.BooleanField(default=False)
    objects = models.Manager()
# endregion Banners
