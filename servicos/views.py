# Pacotes
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Registro
from .forms import UnidadeForm, DepartamentoForm, RegistroForm
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView



class ArticleDetailView(DetailView):

    model = Registro

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    
def dashboard(request):
    
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('account_login'))
    
    registros = Registro.objects.all()
    dados = {
        'registros': registros
    }
    return render(request,'dashboard.html', dados)



def detalhes(request, registro_id):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('account_login'))
    registro = Registro.objects.get(id=registro_id)

    dados = {
        'registro': registro,
        #'unidade': unidade
    }
    return render(request,'detalhes.html ', dados)


def formUnidade(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('account_login'))
    form = UnidadeForm()
    context = {'form': form, 'titulo': 'Cadastro de Unidade'}
    # Cria um variavel do tipo da Classe criande em form.py
    if request.method == 'GET':
        return render(request,'registro.html',context=context)
    else:
        form = UnidadeForm(request.POST)
        if form.is_valid():
            form.save()
            form = UnidadeForm()
            return redirect('dashboard')
        else:
            pass


def formRegistro(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('account_login'))
    form = RegistroForm()
    context = {'form': form, 'titulo': 'Novo Chamado'}
    # Cria um variavel do tipo da Classe criande em form.py
    if request.method == 'GET':
        return render(request,'registro.html',context=context)
    else:
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistroForm()
            messages.add_message(request, messages.SUCCESS, 'Breno')
            form = RegistroForm()
            return redirect('dashboard')
        else:
            pass
class AtualizarRegistro(LoginRequiredMixin,UpdateView):
    
    model = Registro
    fields = "__all__"
    template_name = "registro.html"
    success_url = reverse_lazy('dashboard')
    login_url: reverse_lazy('account_login')

def formDepartamento(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('account_login'))
    form = DepartamentoForm()
    context = {'form': form, 'titulo': 'Cadastro de Departamento'}
    # Cria um variavel do tipo da Classe criande em form.py
    if request.method == 'GET':
        return render(request,'registro.html',context=context)
    else:
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            form = DepartamentoForm()
            messages.add_message(request, messages.SUCCESS, 'Breno')
            return redirect('dashboard')
        else:
            pass



# ggg

# Fim views