from django.shortcuts import render
from django.views.generic import View, UpdateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect

from .models import CustomUser
from .forms import LoginForm, SignUpForm, UserUpdateForm
from django.http import HttpResponseRedirect, HttpResponse


# region Mixins
class CustomAbstractView(View):
    template_name = context = None

    @staticmethod
    def get_context(*args, **kwargs) -> dict:
        return {}

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.context = self.get_context(request, *args, **kwargs)

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name, self.context)


# endregion Mixins

class SignUpView(CustomAbstractView):
    template_name = 'user/signup.html'

    def get_context(self, request):
        self.context = super().get_context()
        self.context['form'] = SignUpForm(request.POST or None)

        return self.context

    def post(self, request):
        self.context = self.get_context(request)
        form = self.context['form']

        if form.is_valid():
            CustomUser.objects.create_user(**form.cleaned_data)
            return HttpResponseRedirect('login')

        return super().post(request)


class LoginView(CustomAbstractView):
    template_name = 'user/login.html'

    def get_context(self, request):
        self.context = super().get_context()
        self.context['form'] = LoginForm(request.POST or None)

        return self.context

    def post(self, request):
        self.context = super().get_context()
        form = self.context['form']

        if form.is_valid():
            username = form.cleaned_data['user_login']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                    request.session.modified = True

                return HttpResponseRedirect('/')

        return super().post(request)


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'user/update.html'
    success_url = '/'

    form_class = UserUpdateForm
