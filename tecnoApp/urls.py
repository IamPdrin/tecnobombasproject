from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('main', views.principal, name="principal"),
    path('login', views.fazerLogin, name="fazerLogin"),
    path('criar-login', views.criarLogin, name='criarLogin'),

    path('adicionar-equip', views.add_equipamento, name="add_equipamento"),
    path('editar/<int:id_equipamento>', views.edt_equipamento, name="edt_equipamento"),
    path('excluir/<int:id_equipamento>', views.excluir_equipamento, name="excluir_equipamento"),
    
    
    path('sel-doc', views.sel_documento, name="sel_documento"),
    path('adicionar-prop', views.add_proposta, name="add_proposta"),
    path('adicionar-orc', views.add_orcamento, name="add_orcamento"),
    path('adicionar-outro', views.add_outros, name="add_outro"),
    path('editar/<int:id_documento>', views.edt_documento, name="edt_documento"),
    path('excluir/<int:id_documento>', views.excluir_documento, name="excluir_documento"),
]