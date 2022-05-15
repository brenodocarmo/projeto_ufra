
from django.urls import path


# from .views import index, detalhes
from . import views

urlpatterns = [
    path('',views.dashboard, name='dashboard'),
    path('detalhes/<int:registro_id>', views.detalhes, name='detalhes'),
    path('unidade/', views.formUnidade, name='formUnidade'),
    path('registro/', views.formRegistro, name='formRegistro'),
    path('departamento/', views.formDepartamento, name='formDepartamento'),
    path('editar/<int:pk>/', views.AtualizarRegistro.as_view(), name='editar'),
    ]