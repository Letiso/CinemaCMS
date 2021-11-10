from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(next_page='/'), name="logout"),
    path('signup', views.SignUpView.as_view(), name="signup"),
    path('user_account', views.SignUpView.as_view(), name="user_account"),
]
