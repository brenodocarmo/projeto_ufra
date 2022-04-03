from django.shortcuts import render
# from django.http import HttpResponse



def index(request):
    return render(request,'index.html')


def detalhes(request):
    return render(request, 'detalhes.html')