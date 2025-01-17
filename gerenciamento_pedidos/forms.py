from django import forms
from django.forms import modelformset_factory
from .models import Cliente, Pedido, ItemPedido, Produto

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'produtos', 'status']
        widgets = {
            'produtos': forms.CheckboxSelectMultiple,  # Permitir seleção de múltiplos produtos
        }
        labels = {
            'cliente': 'Cliente',
            'produtos': 'Produtos',
            'status': 'Status do Pedido',
        }

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in ['pendente', 'em_andamento', 'concluido', 'cancelado']:
            raise forms.ValidationError("Status inválido.")
        return status

    def save(self, commit=True):
        pedido = super().save(commit=False)
        if commit:
            pedido.save()
        return pedido

# Formset para os Itens de Pedido
ItemPedidoFormSet = modelformset_factory(ItemPedido, fields=('produto', 'quantidade'), extra=1)

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'quantidade']  # Corrigido para os campos corretos: 'produto' e 'quantidade'

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco']
        

class AtualizarEstoqueForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'estoque']  # Campos que você quer exibir no formulário

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].queryset = Produto.objects.all()  # Exibir todos os produtos