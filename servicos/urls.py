
from django.urls import path


from .views import index, detalhes

urlpatterns = [
    path('', index, name='index'),
    path('detalhes/', detalhes, name='detalhes'),
    ]