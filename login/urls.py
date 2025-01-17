from django.urls import path
from .views import RegisterView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'  # Registra o namespace

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
