from django.shortcuts import render
from django.views.generic import View, CreateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from .forms import LoginForm, CustomUserCreationForm, CustomUserChangeForm


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'user/login.html', context)

    def post(self, request, *args, **kwargs):
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
        return render(request, 'user/login.html')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/signup.html'




