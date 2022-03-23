from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'user'

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(next_page='/'), name="logout"),
    path('signup', views.SignUpView.as_view(), name="signup"),
    path('<int:pk>/update', login_required(views.UserUpdateView.as_view()), name="update_account"),
    path('<int:pk>/my_tickets', login_required(views.MyTicketsView.as_view()), name="my_tickets"),
]
