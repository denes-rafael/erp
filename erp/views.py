from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
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


@login_required
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


@login_required
def lista_funcionarios(requisicao: HttpRequest):
    if requisicao.method == "GET":
        funcionarios = Funcionario.objects.all()
        return render(
            requisicao,
            template_name="erp/funcionario/lista.html",
            context={"funcionarios": funcionarios},
        )


@login_required
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


@login_required
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


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    template_name = "erp/produtos/novo.html"
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy("erp:home")


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = "erp/produtos/lista.html"
    context_object_name = "produtos"


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "erp/produtos/atualiza.html"
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy("erp:lista_produto")


class ProdutoDetailView(LoginRequiredMixin, DetailView):
    template_name = "erp/produtos/detalhe.html"
    model = Produto
    context_object_name = "produto"

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = "erp/produtos/apaga.html"
    context_object_name = "produto"
    success_url = reverse_lazy("erp:lista_produto")

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None


class VendaCreateView(LoginRequiredMixin, CreateView):
    template_name = "erp/vendas/novo.html"
    model = Venda
    success_url = reverse_lazy("erp:home")
    fields = ["funcionario", "produto"]


class VendaListView(LoginRequiredMixin, ListView):
    model = Venda
    template_name = "erp/vendas/lista.html"
    context_object_name = "vendas"


class VendaDetailView(LoginRequiredMixin, DetailView):
    template_name = "erp/vendas/detalhe.html"
    model = Venda
    context_object_name = "venda"

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            return None


class ErpLoginView(LoginView):
    template_name = "erp/login.html"
    success_url = reverse_lazy("erp:dashboard")
    redirect_authenticated_user = True


class ErpLogoutView(LogoutView):
    template_name = "erp/logout.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "erp/dashboard.html"
