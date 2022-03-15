from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUser(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    GENDERS = (
        ('m', _('Male')),
        ('f', _('Female'))
    )

    LANGUAGES = settings.LANGUAGES

    username_validator = UnicodeUsernameValidator()
    objects = UserManager()

    username = models.CharField(
        _('Login'),
        max_length=50,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _("An user with that username already exists."),
        },
    )
    email = models.EmailField(_('Email address'))
    phone = models.CharField(_('Phone number'), max_length=10)

    first_name = models.CharField(_('First name'), max_length=150, blank=True)
    last_name = models.CharField(_('Last name'), max_length=150, blank=True)

    gender = models.CharField(_('Gender'), max_length=1, choices=GENDERS)
    language = models.CharField(_('Language'), max_length=2, choices=LANGUAGES)
    birth_date = models.DateField(_('Birth date'), default='2000-06-15')
    address = models.CharField(_('Address'), max_length=150, blank=True)

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
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
