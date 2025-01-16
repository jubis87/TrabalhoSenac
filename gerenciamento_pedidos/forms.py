# gerenciamento_pedidos/forms.py
from django import forms
from .models import Cliente, Pedido, ItemPedido  # Importando os modelos Cliente, Pedido e ItemPedido

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente  # Referência ao modelo Cliente
        fields = ['nome', 'email', 'telefone']  # Campos do formulário

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido  # Referenciando o modelo Pedido
        fields = ['cliente', 'produtos', 'status']  # Campos do formulário
        widgets = {
            'produtos': forms.CheckboxSelectMultiple,  # Usando um widget de múltipla seleção para produtos
        }

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in ['pendente', 'em_andamento', 'concluido', 'cancelado']:
            raise forms.ValidationError("Status inválido.")  # Validação do status
        return status

    def save(self, commit=True):
        pedido = super().save(commit=False)  # Não salvar imediatamente
        valor_total = 0
        
        # Calculando o valor total com base nos itens do pedido
        for produto in pedido.produtos.all():
            item = ItemPedido.objects.get(pedido=pedido, produto=produto)
            valor_total += item.get_subtotal()  # Supondo que exista um método get_subtotal() em ItemPedido
        
        pedido.valor_total = valor_total  # Atribuindo o valor total ao pedido
        
        if commit:
            pedido.save()  # Salva o pedido no banco de dados
        
        return pedido
