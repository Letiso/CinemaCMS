# Generated by Django 3.2.9 on 2021-11-08 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('m', 'мужчина'), ('f', 'женщина')], default='', max_length=1, verbose_name='Пол'),
        ),
    ]
