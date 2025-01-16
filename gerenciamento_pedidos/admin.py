from django.contrib import admin
from .models import Cliente, Produto, Pedido, ItemPedido

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'preco')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'produtos', 'quantidade_total', 'data_pedido', 'status')
    list_filter = ('status', 'data_pedido')

    # Método para mostrar os produtos relacionados ao pedido
    def produtos(self, obj):
        return ", ".join([str(item.produto) for item in ItemPedido.objects.filter(pedido=obj)])
    produtos.short_description = 'Produtos'

    # Método para mostrar a quantidade total dos produtos no pedido
    def quantidade_total(self, obj):
        return sum([item.quantidade for item in ItemPedido.objects.filter(pedido=obj)])
    quantidade_total.short_description = 'Quantidade Total'
