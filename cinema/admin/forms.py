from django import forms
from user.forms import UserUpdateForm


from copy import copy


class ExtendedUserUpdateForm(UserUpdateForm):

    Meta = copy(UserUpdateForm.Meta)
    Meta.fields += ('is_staff', 'is_superuser')
