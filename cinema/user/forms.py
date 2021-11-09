from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


class LoginForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Имя пользователя или почта',
                'autofocus': True
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': '•' * 15,
            }),
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователя {username} еще не существует')
        user = CustomUser.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'gender', 'birth_date')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Иван',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Иванов',
            }),
            'gender': forms.Select(attrs={
                'class': 'custom-select mr-sm-2 my-2',
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control mb-2',
            }),
            'password1': forms.PasswordInput(attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Введите пароль',
            }),
            'password2': forms.PasswordInput(attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Введите пароль',
            }),
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('is_staff', 'first_name', 'last_name', 'gender', 'birth_date', 'username', 'email', )
