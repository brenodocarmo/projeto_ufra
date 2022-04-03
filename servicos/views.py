from django.shortcuts import render


def index(request):
    return render(request,'index.html')


def detalhes(request):
    return render(request, 'detalhes.html')