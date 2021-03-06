# Generated by Django 3.2.9 on 2021-11-17 11:47

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, upload_to='user/profile/', verbose_name='Аватар')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=50, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Логин')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('phone', models.CharField(blank=True, max_length=10, verbose_name='Номер телефона')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('gender', models.CharField(choices=[('m', 'Мужской'), ('f', 'Женский')], max_length=1, verbose_name='Пол')),
                ('language', models.CharField(choices=[('ru', 'Русский'), ('ua', 'Українська'), ('en', 'English')], max_length=2, verbose_name='Язык')),
                ('birth_date', models.DateField(default='2000-06-15', verbose_name='Дата рождения')),
                ('address', models.CharField(blank=True, max_length=150, verbose_name='Адрес')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.customuserprofile')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
