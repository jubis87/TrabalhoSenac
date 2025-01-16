from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.listar_pedidos), name='listar_pedidos'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastrar_pedido/', views.cadastrar_pedido, name='cadastrar_pedido'),
    path('cadastrar_cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('cadastrar_pedido/', views.cadastrar_pedido, name='cadastrar_pedido'),
    path('cadastrar_cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
]
