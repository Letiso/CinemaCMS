from django import forms

from .models import CustomUser


class LoginForm(forms.ModelForm):

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

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        labels = {
            'username': 'Логин',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Имя пользователя или почта',
                'autofocus': True
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': '•' * 15,
            }),
        }


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
            'phone': forms.NumberInput(attrs={
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
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control mb-2',
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Приморский район, ул. Екатерининская, 156',
            }),
        }
