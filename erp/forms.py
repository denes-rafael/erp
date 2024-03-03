from django import forms

from erp.models import Funcionario, Produto


# class FuncionarioForm(forms.Form):
#     nome = forms.CharField(max_length=30, required=True)
#     sobrenome = forms.CharField(max_length=50, required=True)
#     cpf = forms.CharField(max_length=11, required=True)
#     email_corporativo = forms.EmailField(max_length=50, required=True)
#     remuneracao = forms.DecimalField(max_digits=6, decimal_places=2, required=True)


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ["nome", "sobrenome", "cpf", "email_corporativo", "remuneracao"]


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"
        labels = {
            "descricao": "Descrição",
            "preco": "Preço",
        }
