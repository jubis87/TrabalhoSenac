from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Página inicial
    path('', login_required(views.listar_pedidos), name='listar_pedidos'),

    # Listagem de clientes
    path('listar_clientes/', login_required(views.listar_clientes), name='listar_clientes'),

    # Login e logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Cadastro de pedidos e clientes
    path('cadastrar_pedido/', login_required(views.cadastrar_pedido), name='cadastrar_pedido'),
    path('cadastrar_cliente/', login_required(views.cadastrar_cliente), name='cadastrar_cliente'),

    # Dashboard de estatísticas
    path('dashboard/', login_required(views.dashboard), name='dashboard'),

    # Listagem de produtos
    path('listar_produtos/', login_required(views.listar_produtos), name='listar_produtos'),

    # Cadastro de itens de pedidos (associado a um pedido específico)
    path('pedido/<int:pedido_id>/cadastrar_item/', login_required(views.cadastrar_item), name='cadastrar_item'),

    # Cadastro de produto
    path('cadastrar-produto/', login_required(views.cadastro_produto), name='cadastrar_produto'),  # Corrigido o nome da URL

    # Atualização de estoque
    path('atualizar_estoque/', login_required(views.atualizar_estoque), name='atualizar_estoque'),
]
