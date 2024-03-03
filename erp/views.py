from django.db.models import QuerySet
from django.db.models.base import Model as Model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import Http404, HttpRequest, HttpResponseRedirect
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)

from django.views.generic.detail import DetailView

from erp.forms import FuncionarioForm, ProdutoForm
from erp.models import Funcionario, Produto, Venda


# def home(requisicao: HttpRequest):
#     if requisicao.method == "GET":
#         return render(requisicao, template_name="erp/index.html")


class HomeView(TemplateView):
    template_name = "erp/index.html"


def cria_funcionario(requisicao: HttpRequest):
    if requisicao.method == "GET":
        form = FuncionarioForm()
        return render(
            requisicao,
            template_name="erp/funcionario/formulario.html",
            context={"form": form},
        )
    elif requisicao.method == "POST":
        form = FuncionarioForm(requisicao.POST)

        if form.is_valid():
            # funcionario = Funcionario(
            #     nome=form.cleaned_data.get('nome'),
            #     sobrenome=form.cleaned_data.get('sobrenome'),
            #     cpf=form.cleaned_data.get('cpf'),
            #     email_corporativo=form.cleaned_data.get('email_corporativo'),
            #     remuneracao=form.cleaned_data.get('remuneracao'),
            # )
            funcionario = Funcionario(**form.cleaned_data)

            funcionario.save()

            return HttpResponseRedirect(redirect_to="/")


def lista_funcionarios(requisicao: HttpRequest):
    if requisicao.method == "GET":
        funcionarios = Funcionario.objects.all()
        return render(
            requisicao,
            template_name="erp/funcionario/lista.html",
            context={"funcionarios": funcionarios},
        )


def busca_funcionario_id(requisicao: HttpRequest, pk: int):
    if requisicao.method == "GET":

        try:
            funcionario = Funcionario.objects.get(pk=pk)
        except Funcionario.DoesNotExist:
            funcionario = None

        return render(
            requisicao,
            template_name="erp/funcionario/detalhe.html",
            context={"funcionario": funcionario},
        )


def atualiza_funcionario(requisicao: HttpRequest, pk: int):
    if requisicao.method == "GET":
        funcionario = Funcionario.objects.get(pk=pk)
        form = FuncionarioForm(instance=funcionario)

        return render(
            requisicao,
            template_name="erp/funcionario/atualiza.html",
            context={"form": form},
        )

    elif requisicao.method == "POST":
        funcionario = Funcionario.objects.get(pk=pk)
        form = FuncionarioForm(requisicao.POST, instance=funcionario)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(redirect_to=f"/funcionarios/{pk}/detalhe")


class ProdutoCreateView(CreateView):
    template_name = "erp/produtos/novo.html"
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy("erp:home")


class ProdutoListView(ListView):
    model = Produto
    template_name = "erp/produtos/lista.html"
    context_object_name = "produtos"


class ProdutoUpdateView(UpdateView):
    template_name = "erp/produtos/atualiza.html"
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy("erp:lista_produto")


class ProdutoDetailView(DetailView):
    template_name = "erp/produtos/detalhe.html"
    model = Produto
    context_object_name = "produto"

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None


class ProdutoDeleteView(DeleteView):
    model = Produto
    template_name = "erp/produtos/apaga.html"
    context_object_name = "produto"
    success_url = reverse_lazy("erp:lista_produto")

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None


class VendaCreateView(CreateView):
    template_name = "erp/vendas/novo.html"
    model = Venda
    success_url = reverse_lazy("erp:home")
    fields = ["funcionario", "produto"]


class VendaListView(ListView):
    model = Venda
    template_name = "erp/vendas/lista.html"
    context_object_name = "vendas"


class VendaDetailView(DetailView):
    template_name = "erp/vendas/detalhe.html"
    model = Venda
    context_object_name = "venda"

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None    