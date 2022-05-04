from django.shortcuts import render
from .models import Registro, Unidade


def index(request):
    registros = Registro.objects.all()

    dados = {
        'registros': registros
    }
    return render(request,'index.html', dados)


def detalhes(request, registro_id):

    registro = Registro.objects.get(id=registro_id)
    unidade = Unidade.objects.get(id=registro_id)

    dados = {
        'registro': registro,
        'unidade': unidade
    }
    return render(request,'detalhes.html ', dados)


def login(request):
    return render(request, 'login.html')