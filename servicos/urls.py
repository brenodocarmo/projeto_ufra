
from django.urls import path


# from .views import index, detalhes
from . import views

urlpatterns = [
    #path('detalhes/<int:pk>/', views.DetalhesRegistro.as_view(), name='detalhes'),
    path('detalhes/<int:pk>/', views.detalhes, name='detalhes'),
    path('',views.dashboard, name='dashboard'),
    path('unidade/', views.CriarUnidade.as_view(), name='formUnidade'),
    path('departamento/', views.CriarDepartamento.as_view(), name='formDepartamento'),
    path('editar/<int:pk>/', views.AtualizarRegistro.as_view(), name='editar'),
    path('report/', views.report, name='report'),
    path('registro/',views.CriarRegistro.as_view(),name='formRegistro'),
    path('404/',views.erro_404,name='erro_404'),
    ]