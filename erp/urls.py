from django.urls import path
from django.conf.urls.static import static
from core import settings
from erp.views import *

app_name = "erp"

urlpatterns = [
    # path("", home),
    path("", HomeView.as_view(), name="home"),
    #
    # Dashboard
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    #
    # Login
    path("login/", ErpLoginView.as_view(), name="login"),
    #
    # Logout
    path("logout/", ErpLogoutView.as_view(), name="logout"),
    #
    # Funcionários
    path("funcionarios/", lista_funcionarios),
    path("funcionarios/novo/", cria_funcionario),
    path("funcionarios/<pk>/detalhe/", busca_funcionario_id),
    path("funcionarios/<pk>/atualiza/", atualiza_funcionario),
    #
    # Produtos
    path("produtos/", ProdutoListView.as_view(), name="lista_produto"),
    path("produtos/novo/", ProdutoCreateView.as_view(), name="cria_produto"),
    path("produtos/<pk>/detalhe/", ProdutoDetailView.as_view(), name="detalhe_produto"),
    path(
        "produtos/<pk>/atualiza/", ProdutoUpdateView.as_view(), name="atualiza_produto"
    ),
    path("produtos/<pk>/apaga/", ProdutoDeleteView.as_view(), name="apaga_produto"),
    #
    # Vendas
    path("vendas/", VendaListView.as_view(), name="lista_venda"),
    path("vendas/novo/", VendaCreateView.as_view(), name="cria_venda"),
    path("vendas/<pk>/detalhe/", VendaDetailView.as_view(), name="detalhe_venda"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
