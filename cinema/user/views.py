from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, CustomUserChangeForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main')
    template_name = 'user/signup.html'


class SignInView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('main')
    template_name = 'user/signin.html'

