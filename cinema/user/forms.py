from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        label=_('Repeat password'),
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Chosen username is already linked to another account'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Chosen email is already linked to another account'))
        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError(_('Passwords not match'))

        del self.cleaned_data['confirm_password']   # Because it's not necessary already

        return self.cleaned_data

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'confirm_password', 'email', 'phone',
                  'first_name', 'last_name', 'gender', 'language', 'birth_date', 'address', )
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@email.com',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '095-123-45-15',
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': _('John'),
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': _('Brain'),
            }),
            'gender': forms.Select(attrs={
                'class': 'custom-select mr-sm-2 my-2',
            }),
            'language': forms.Select(attrs={
                'class': 'custom-select mr-sm-2 my-2',
            }),
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'type': 'date',
                'class': 'form-control mb-2',
            }),
            'address': forms.TextInput(attrs={
                'placeholder': _(''),  # Приморский район, ул. Екатерининская, 156  # TODO
            }),
        }


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required=False
    )
    confirm_password = forms.CharField(
        label=_('Repeat password'),
        widget=forms.PasswordInput,
        required=False
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(_('Chosen username is already linked to another account'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_('Chosen email is already linked to another account'))
        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        password_is_valid = password == confirm_password

        if password and not password_is_valid:
            raise forms.ValidationError(_('Passwords not match'))
        else:
            # this step means that password wasn't changed actually
            # and there's no need in password update
            del self.cleaned_data['password']

        return self.cleaned_data

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password', 'confirm_password',
                  'first_name', 'last_name', 'gender', 'language', 'birth_date', 'address')
        widgets = {
            'gender': forms.Select(attrs={
                'class': 'custom-select mr-sm-2 my-2',
            }),
            'language': forms.Select(attrs={
                'class': 'custom-select mr-sm-2 my-2',
            }),
            'birth_date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': 'date',
                'class': 'form-control mb-2',
            }),
            'address': forms.TextInput(attrs={
                'placeholder': _(''),   # Приморский район, ул. Екатерининская, 156  # TODO
            }),
        }


class LoginForm(forms.Form):
    user_login = forms.CharField(
        label=_('Login'),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Username or email'),
                'autofocus': True
            }
        )
    )
    password = forms.CharField(
        label=_('Password'),
        max_length=256,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '•' * 15,
            }
        )
    )
    remember_me = forms.BooleanField(
        label=_('Remember me'),
        required=False,
        widget=forms.CheckboxInput()
    )
    user_model = CustomUser.objects

    def clean_user_login(self):
        user_login = self.cleaned_data['user_login']

        if "@" in user_login:
            if not self.user_model.filter(email=user_login).exists():
                raise forms.ValidationError(_('User with the email') + f' "{user_login}" ' + 'does not exists')

            user_login = self.user_model.get(email=user_login).username
        else:
            if not self.user_model.filter(username=user_login).exists():
                raise forms.ValidationError(_('User') + f' "{user_login}" ' + 'does not exists')

        return user_login

    def clean(self):
        user_login = self.cleaned_data['user_login']
        password = self.cleaned_data['password']

        user = CustomUser.objects.filter(username=user_login).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError(_('Invalid password'))

        return self.cleaned_data
