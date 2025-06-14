from django.urls import path
from .views import register_view, login_view, logout_view, dashboard
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", views.register_view, name="register"),
    path("", dashboard, name="dashboard"),
    path('search_students/', views.search_students, name='search_students'),
]