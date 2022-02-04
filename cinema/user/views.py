from django.shortcuts import render
from django.views.generic import View, UpdateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect

from .models import CustomUser
from .forms import LoginForm, SignUpForm, UserUpdateForm


class SignUpView(View):
    @staticmethod
    def get(request):
        form = SignUpForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'user/signup.html', context)

    @staticmethod
    def post(request):
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            del form.cleaned_data['confirm_password']
            new_user = CustomUser.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'user/signup.html', context)


class LoginView(View):
    @staticmethod
    def get(request):
        form = LoginForm(request.POST or None)
        context = {
            'title': 'Авторизация',
            'form': form,
        }
        return render(request, 'user/login.html', context)

    @staticmethod
    def post(request):
        form = LoginForm(request.POST or None)
        context = {
            'title': 'Авторизация',
            'form': form,

        }
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'user/login.html', context)


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'user/update.html'
    success_url = '/'

    form_class = UserUpdateForm
