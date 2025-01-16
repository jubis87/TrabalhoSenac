# gerenciamento_pedidos/views.py
from django.shortcuts import render, redirect
from .forms import PedidoForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Pedido  # Adicione esta linha para importar o modelo Pedido
from django.core.paginator import Paginator
from .forms import ClienteForm



def listar_pedidos(request):
    pedidos = Pedido.objects.all()  # Agora o Pedido está definido
    return render(request, 'gerenciamento_pedidos/listar_pedidos.html', {'pedidos': pedidos})

@login_required
def cadastrar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pedidos')  # Redireciona para a lista de pedidos
    else:
        form = PedidoForm()
    return render(request, 'gerenciamento_pedidos/cadastrar_pedido.html', {'form': form})


def listar_pedidos(request):
    pedidos_list = Pedido.objects.all()  # Obtém todos os pedidos
    paginator = Paginator(pedidos_list, 10)  # 10 pedidos por página
    page_number = request.GET.get('page')
    pedidos = paginator.get_page(page_number)
    
    return render(request, 'gerenciamento_pedidos/listar_pedidos.html', {'pedidos': pedidos})


# gerenciamento_pedidos/views.py
from .forms import ClienteForm

def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pedidos')  # Redireciona para a lista de pedidos após criar o cliente
    else:
        form = ClienteForm()
    return render(request, 'gerenciamento_pedidos/cadastrar_cliente.html', {'form': form})


# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pedido
from .forms import PedidoForm

def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'listar_pedidos.html', {'pedidos': pedidos})

@login_required
def cadastrar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pedidos')
    else:
        form = PedidoForm()
    return render(request, 'cadastrar_pedido.html', {'form': form})
