
from django.urls import path


# from .views import index, detalhes
from . import views

urlpatterns = [
    # path('', index, name='index'),
    # path('detalhes/', detalhes, name='detalhes'),

    path('', views.index, name='index'),
    path('login/', views.login, name='logon'),
    path('<int:registro_id>', views.detalhes, name='detalhes'),
    # path('<int:registro.id>', detalhes, name='detalhes'),
    ]