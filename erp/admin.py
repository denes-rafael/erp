from django.contrib import admin

from erp.models import Funcionario, Produto, Venda


class FuncionarioAdmin(admin.ModelAdmin): ...


class ProdutoAdmin(admin.ModelAdmin): ...


class VendaAdmin(admin.ModelAdmin): ...


admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Venda, VendaAdmin)
