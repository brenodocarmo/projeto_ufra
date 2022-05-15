
from django.urls import path


# from .views import index, detalhes
from . import views

urlpatterns = [
    path('detalhes/<int:pk>/', views.DetalhesRegistro.as_view(), name='detalhes'),
    path('',views.dashboard, name='dashboard'),
    path('unidade/', views.formUnidade, name='formUnidade'),
    path('registro/', views.formRegistro, name='formRegistro'),
    path('departamento/', views.formDepartamento, name='formDepartamento'),
    path('editar/<int:pk>/', views.AtualizarRegistro.as_view(), name='editar'),
    ]