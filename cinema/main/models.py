from django.db import models


# region Banners
banners_path = 'main/index/banners'


def background_path(instance, filename):
    filename = 'background.' + filename.split('.')[-1]
    return '{0}/{1}'.format(banners_path, filename)


class TopBanner(models.Model):
    image = models.ImageField('Баннер', upload_to=f'{banners_path}/top')
    is_active = models.BooleanField(default=False)


class BackgroundImage(models.Model):
    image = models.ImageField('Фоновое изображение', upload_to=background_path)
    is_active = models.BooleanField(help_text='Если не отмечено, вместо картинки фон будет сплошным стандартным цветом',
                                    default=False)
    color = models.TextField(default='#f4f6f9')
    objects = models.Manager()


class NewsBanner(models.Model):
    image = models.ImageField('Баннер', upload_to=f'{banners_path}/news')
    is_active = models.BooleanField(default=False)
# endregion Banners
