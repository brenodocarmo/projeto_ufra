# Pacotes
import smtplib
from telnetlib import STATUS
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Registro
from .forms import UnidadeForm, DepartamentoForm, RegistroForm
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.core.exceptions import ImproperlyConfigured
from users.models import User
from email.message import EmailMessage

# Configaraçoes de e-mail SMTP
def SendSMTPEmail(destinatario,assunto,mensagem):

    # Login e senha
    EMAIL_ADRESS =  'scsti.suporte@gmail.com'
    EMAIL_PASSWORD = 'scstifdsa4321'
    EMAIL_SMTP_SERVER = 'smtp.gmail.com'
    EMAIL_SMTP_PORT = 465

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL_ADRESS
    msg['To'] = destinatario
    msg.set_content(mensagem)

    with smtplib.SMTP_SSL(EMAIL_SMTP_SERVER,EMAIL_SMTP_PORT) as smtp:
        smtp.login(EMAIL_ADRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)






class DetalhesRegistro(LoginRequiredMixin,DetailView):


    login_url: reverse_lazy('account_login')

    model = Registro
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class AtualizarRegistro(LoginRequiredMixin,UpdateView):

    login_url: reverse_lazy('account_login')

    model = Registro
    fields = ["titulo","descricao","departamento_id","status","patrimonio"]
    template_name = "registro.html"
    success_url = reverse_lazy('dashboard')

    status_before = ''
    status_after = ''
    email_to_send = ''
    chamado = ''

    def post(self, request, *args, **kwargs):

        # Email sender status before
        self.status_before = self.get_object().status
        self.chamado = self.get_object().titulo
        # id de quem criou o chamdo
        user_id = self.get_object().user_id
        user_object = User.objects.filter(id=user_id).values('email')
        user_dic = list(user_object)[0]
        self.email_to_send = user_dic['email']
        
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            # Email sender status after
            self.status_after = self.get_object().status

            # Menssgem de E-mail
            email_message = f'O Status do chamado: {self.chamado} foi Atualizado de {self.status_before} para {self.status_after}'

            # Envio do E-mail
            SendSMTPEmail(self.email_to_send,'Atualização de Status do Chamado',email_message)

            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")

def dashboard(request):
    
    #if not request.user.is_authenticated:
    #    return redirect(reverse_lazy('account_login'))
    
    registros = Registro.objects.all()
    registros.order_by('id')
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
            user_id = request.user.id
            last = Registro.objects.last()
            last.user_id = user_id
            last.save()
            form = RegistroForm()
            return redirect('dashboard')
        else:
            pass


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

def report(request):
    
    class obj ():
        status_chamado = ''
        quantidade = ''
        def __init__(self,status_chamado,quantidade):
            self.status = status_chamado
            self.quantidade = quantidade
            
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('account_login'))
    registros = []


    STATUS_REGISTRO = ['Pendente','Em andamento','Finalizado', 'Cancelado']
    
    
    for i in STATUS_REGISTRO:
        registros.append(obj(i,Registro.objects.filter(status=i).count))
    dados = {
        'dados':registros
    }
    return render(request,'report.html', dados)

# Fim views