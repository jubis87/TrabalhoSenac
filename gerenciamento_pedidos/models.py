from django.db import models
from django.utils import timezone
from datetime import timedelta

# Modelo para o Cliente
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    endereco = models.TextField(null=True, blank=True)  # Campo opcional

    def __str__(self):
        return self.nome

# Modelo para o Produto
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

    def atualizar_estoque(self, quantidade):
        """Atualiza o estoque após o pedido."""
        if self.estoque >= quantidade:
            self.estoque -= quantidade
            self.save()
        else:
            raise ValueError("Estoque insuficiente para esta quantidade.")

# Tabela intermediária para o relacionamento de muitos para muitos entre Pedido e Produto
class ItemPedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # Preço do produto no momento do pedido

    def get_subtotal(self):
        """Calcula o subtotal do item (quantidade * preço unitário)."""
        return self.quantidade * self.preco_unitario

    def save(self, *args, **kwargs):
        # Atualiza o estoque do produto quando o item é salvo
        if self.pk is None:  # Só atualiza o estoque quando o item for criado (não editado)
            self.produto.atualizar_estoque(self.quantidade)
        else:
            # Se o item já existe, atualize o estoque considerando a diferença na quantidade
            old_item = ItemPedido.objects.get(pk=self.pk)
            quantidade_diferenca = self.quantidade - old_item.quantidade
            if quantidade_diferenca != 0:
                self.produto.atualizar_estoque(quantidade_diferenca)
        super().save(*args, **kwargs)

# Modelo para o Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through=ItemPedido)  # Relacionamento de muitos para muitos
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ], default='pendente')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_pedido = models.DateTimeField(auto_now_add=True)

    def get_valor_total(self):
        """Calcula o valor total do pedido com base nos itens."""
        return sum(item.get_subtotal() for item in self.itempedido_set.all())

    def save(self, *args, **kwargs):
        # Recalcular o valor total antes de salvar
        if not self.pk:  # Se ainda não tem uma chave primária
            super().save(*args, **kwargs)  # Salva o pedido sem o valor total (para gerar o ID)
            self.valor_total = self.get_valor_total()  # Calcula o valor total
        else:
            self.valor_total = self.get_valor_total()  # Calcula o valor total se já existir o pedido
        super().save(*args, **kwargs)  # Salva o pedido com o valor total

    def excluir(self):
        """Exclui pedidos antigos (mais de 30 dias)."""
        if self.data_pedido < timezone.now() - timedelta(days=30):
            self.delete()

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome}"
    
    @classmethod
    def excluir_pedidos_antigos(cls):
        """Exclui todos os pedidos com mais de 30 dias."""
        cls.objects.filter(data_pedido__lt=timezone.now() - timedelta(days=30)).delete()
