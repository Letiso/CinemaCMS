from django.shortcuts import render
from django.views.generic import View, CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from .models import CustomUser
from .forms import LoginForm, SignUpForm


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
            new_user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                gender=form.cleaned_data['gender'],
                language=form.cleaned_data['language'],
                birth_date=form.cleaned_data['birth_date'],
                address=form.cleaned_data['address'],
            )
            login(request, new_user)
            return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'user/signup.html', context)
