from django.db import models


class BackgroundImage(models.Model):
    image = models.ImageField('Баннер', upload_to='main/home/banners/')
    status = models.BooleanField(default=False)


class TopBanner(models.Model):
    image = models.ImageField('Баннер', upload_to='main/home/banners/')
    status = models.BooleanField(default=False)
