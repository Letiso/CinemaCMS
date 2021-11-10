from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUser(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    GENDERS = (
        ('m', 'мужской'),
        ('f', 'женский')
    )
    LANGUAGES = (
        ('ru', 'Русский'),
        ('ua', 'Українська'),
        ('en', 'English')
    )
    username_validator = UnicodeUsernameValidator()
    objects = UserManager()

    username = models.CharField(
        'Логин',
        max_length=50,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True)
    phone = models.CharField('Номер телефона', max_length=12, blank=True)

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    gender = models.CharField('Пол', max_length=1, choices=GENDERS, default='')
    language = models.CharField('Язык', max_length=2, choices=LANGUAGES, default='')
    birth_date = models.DateField('Дата рождения', default='2000-06-15')
    address = models.CharField('Адрес', max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        )
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
