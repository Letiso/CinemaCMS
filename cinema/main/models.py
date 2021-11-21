from django.db import models


# region Banners
class TopBanner(models.Model):
    image = models.ImageField('Баннер', upload_to='main/index/banners/top')
    is_active = models.BooleanField(default=False)


class BackgroundImage(models.Model):
    image = models.ImageField('Фоновое изображение', upload_to='main/index/background/')
    status = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


class NewsBanner(models.Model):
    image = models.ImageField('Баннер', upload_to='main/index/banners/top')
    is_active = models.BooleanField(default=False)
# endregion Banners
