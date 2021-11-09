from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name="login"),
    path('signup', views.SignUpView.as_view(), name="signup"),
    path('user_account', views.SignUpView.as_view(), name="user_account"),
]
