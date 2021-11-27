# Generated by Django 3.2.9 on 2021-11-22 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20211121_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backgroundimage',
            name='is_active',
        ),
        migrations.AddField(
            model_name='backgroundimage',
            name='color',
            field=models.TextField(default='#f4f6f9'),
        ),
        migrations.AlterField(
            model_name='backgroundimage',
            name='image',
            field=models.ImageField(upload_to='main/index/banners/background/', verbose_name='Фоновое изображение'),
        ),
        migrations.AlterField(
            model_name='newsbanner',
            name='image',
            field=models.ImageField(upload_to='main/index/banners/news', verbose_name='Баннер'),
        ),
        migrations.AlterField(
            model_name='topbanner',
            name='image',
            field=models.ImageField(upload_to='main/index/banners/top', verbose_name='Баннер'),
        ),
    ]