from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PedidoForm, ItemPedidoFormSet, ClienteForm
from .models import Pedido, ItemPedido, Cliente, Produto
from django.db.models import Sum
from .forms import ItemPedidoForm
from django.contrib import messages
from .forms import AtualizarEstoqueForm
from .forms import AtualizarEstoqueForm


# View para listar todos os pedidos
@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.all()  # Obtém todos os pedidos
    return render(request, 'gerenciamento_pedidos/listar_pedidos.html', {'pedidos': pedidos})

# View para listar todos os produtos
def listar_produtos(request):
    produtos = Produto.objects.all()  # Obtém todos os produtos cadastrados
    return render(request, 'gerenciamento_pedidos/listar_produtos.html', {'produtos': produtos})

# View para cadastrar um novo pedido
@login_required
def cadastrar_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        item_formset = ItemPedidoFormSet(request.POST)

        # Verifica se o formulário e o formset são válidos
        if pedido_form.is_valid() and item_formset.is_valid():
            pedido = pedido_form.save(commit=False)  # Não salva o pedido imediatamente, para poder modificar

            # Salva o pedido, para que ele tenha um ID (PK)
            pedido.save()

            # Agora que o pedido tem uma chave primária, salva os itens
            itens = item_formset.save(commit=False)
            for item in itens:
                item.pedido = pedido  # Associa o item ao pedido
                item.save()  # Salva o item

            # Recalcula o valor total e salva novamente o pedido com o valor total
            pedido.valor_total = pedido.get_valor_total()  # Supondo que você tenha esse método
            pedido.save()

            return redirect('listar_pedidos')  # Redireciona para a lista de pedidos
    else:
        pedido_form = PedidoForm()
        item_formset = ItemPedidoFormSet(queryset=ItemPedido.objects.none())  # Inicializa o formset de itens

    return render(request, 'gerenciamento_pedidos/cadastrar_pedido.html', {
        'pedido_form': pedido_form,
        'item_formset': item_formset,
    })


# View para cadastrar um novo cliente
@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o cliente
            return redirect('listar_clientes')  # Redireciona para a lista de clientes após criar o cliente
    else:
        form = ClienteForm()
    return render(request, 'gerenciamento_pedidos/cadastrar_cliente.html', {'form': form})

# View para listar todos os clientes
@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()  # Obtém todos os clientes
    return render(request, 'gerenciamento_pedidos/listar_clientes.html', {'clientes': clientes})

# View para o dashboard com informações gerais
@login_required
def dashboard(request):
    total_pedidos = Pedido.objects.count()
    total_clientes = Cliente.objects.count()
    total_produtos = Produto.objects.count()
    valor_total_pedidos = Pedido.objects.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    pedidos = Pedido.objects.all()  # Obtém todos os pedidos

    context = {
        'total_pedidos': total_pedidos,
        'total_clientes': total_clientes,
        'total_produtos': total_produtos,
        'valor_total_pedidos': valor_total_pedidos,
        'pedidos': pedidos,  # Passando a lista de pedidos para o template
    }

    return render(request, 'gerenciamento_pedidos/dashboard.html', context)

# View para cadastrar um novo item de pedido
@login_required
def cadastrar_item(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)  # Obtém o pedido ao qual o item será associado

    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido  # Associa o item ao pedido
            item.save()  # Salva o novo item
            return redirect('listar_pedidos')  # Redireciona para a lista de pedidos após o cadastro
    else:
        form = ItemPedidoForm()  # Cria um formulário vazio

    return render(request, 'gerenciamento_pedidos/cadastrar_item.html', {'form': form, 'pedido': pedido})

# View para exibir o formulário de cadastro de produto
def cadastro_produto(request):
    if request.method == 'POST':
        nome_produto = request.POST.get('nome_produto')
        descricao_produto = request.POST.get('descricao_produto')
        preco_produto = request.POST.get('preco_produto')

        # Validação do formulário
        if nome_produto and descricao_produto and preco_produto:
            novo_produto = Produto(
                nome=nome_produto,
                descricao=descricao_produto,
                preco=preco_produto
            )
            novo_produto.save()
            return redirect('listar_produtos')  # Redireciona para a página de listagem de produtos
        else:
            # Se algum campo obrigatório não foi preenchido, exibe uma mensagem de erro
            return render(request, 'gerenciamento_pedidos/cadastro_produto.html', {
                'error': 'Todos os campos são obrigatórios.'
            })

    return render(request, 'gerenciamento_pedidos/cadastro_produto.html')  # Exibe o formulário de cadastro


def atualizar_estoque(request):
    if request.method == 'POST':
        form = AtualizarEstoqueForm(request.POST)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Estoques de {produto.nome} atualizado para {produto.estoque}.')
            return redirect('atualizar_estoque')
        else:
            messages.error(request, 'Erro ao atualizar o estoque. Tente novamente.')
    else:
        form = AtualizarEstoqueForm()

    produtos = Produto.objects.all()
    return render(request, 'gerenciamento_pedidos/atualizar_estoque.html', {'form': form, 'produtos': produtos})