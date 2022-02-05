from django import forms

from .models import CustomUser  # , CustomUserProfile


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Выбраный логин уже занят')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Данная почта уже привязана к другой учетной записи')
        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        del self.cleaned_data['confirm_password'] # Because it's not necessary already

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
                'placeholder': 'Иван',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Иванов',
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
                'placeholder': 'Приморский район, ул. Екатерининская, 156',
            }),
        }


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        required=False
    )
    confirm_password = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput,
        required=False
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Выбраный логин уже занят')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Данная почта уже привязана к другой учетной записи')
        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        password_is_valid = password == confirm_password

        if password and not password_is_valid:
            raise forms.ValidationError('Пароли не совпадают')
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
                'placeholder': 'Приморский район, ул. Екатерининская, 156',
            }),
        }


class LoginForm(forms.Form):
    user_login = forms.CharField(
        label='Логин',
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя пользователя или почта',
                'autofocus': True
            }
        )
    )
    password = forms.CharField(
        label='Пароль',
        max_length=256,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '•' * 15,
            }
        )
    )
    remember_me = forms.BooleanField(
        label='Запомнить меня',
        required=False,
        widget=forms.CheckboxInput()
    )
    user_model = CustomUser.objects

    def clean_user_login(self):
        user_login = self.cleaned_data['user_login']

        if "@" in user_login:
            if not self.user_model.filter(email=user_login).exists():
                raise forms.ValidationError(f'Пользователь с почтой "{user_login}" не найден')

            user_login = self.user_model.get(email=user_login).username
        else:
            if not self.user_model.filter(username=user_login).exists():
                raise forms.ValidationError(f'Пользователь "{user_login}" не найден')

        return user_login

    def clean(self):
        user_login = self.cleaned_data['user_login']
        password = self.cleaned_data['password']

        user = CustomUser.objects.filter(username=user_login).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')

        return self.cleaned_data
