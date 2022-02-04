from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(next_page='/'), name="logout"),
    path('signup', views.SignUpView.as_view(), name="signup"),
    path('<int:pk>/update', login_required(views.UserUpdateView.as_view()), name="update_account"),

    # path('<int:pk>/delete', login_required(views.SignUpView.as_view()), name="delete_account"),
    # path('account', login_required(views.user_account), name="account"),
]
