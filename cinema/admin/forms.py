from django import forms
from django.contrib.auth import get_user_model
from user.forms import UserUpdateForm


class FullUserUpdateForm(UserUpdateForm):
    UserUpdateForm.Meta.fields += ('is_staff', 'is_superuser')
