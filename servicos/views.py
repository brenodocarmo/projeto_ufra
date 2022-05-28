# Pacotes
import smtplib
from telnetlib import STATUS
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from matplotlib.style import context
from requests import request
from .models import Departamento, Registro, Unidade
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.core.exceptions import ImproperlyConfigured
from users.models import User
from email.message import EmailMessage
from django.views.generic import CreateView
from django.utils.decorators import classonlymethod


LOGIN_URL = 'account_login'



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


############## Cadastro de Objetos #####################

class CriarRegistro(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy(LOGIN_URL)
    model = Registro
    fields = ['titulo','descricao','departamento_id','patrimonio']
    template_name = 'registro.html'
    extra_context = {'titulo':'Registrar Chamado'}
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # Coloca o Usuario Atual na instancia do Objeto
        form.instance.user = self.request.user
        url = super().form_valid(form)
        return url

class CriarDepartamento(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy(LOGIN_URL)
    model = Departamento
    fields = "__all__"
    template_name = 'registro.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'titulo':'Cadastrar Departamento'}

class CriarUnidade(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy(LOGIN_URL)
    model = Unidade
    fields = "__all__"
    template_name = 'registro.html'
    success_url = reverse_lazy('dashboard')
    extra_context = {'titulo':'Cadastrar Unidade'}


############# Visualizar ####################

'''
class DetalhesRegistro(LoginRequiredMixin,DetailView):
    login_url: reverse_lazy('account_login')
    model = Registro
'''

def detalhes(request,pk):

    obj_dic = list(Registro.objects.filter(id=pk).values())[0]

    if request.user.is_superuser == False:
        if obj_dic['user_id'] != request.user.id:
            return render(request,'no_acces.html')
    dados = {
    # Seleciona o obj no BD pela Primary Key => PK
        'object': Registro.objects.filter(id=pk).first
    }
    return render(request,'servicos/registro_detail.html',context=dados)


################## Atualizar ###################

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

    def get(self, request, *args, **kwargs):
        if self.get_object().user_id != request.user.id and request.user.is_superuser == False:
            return render(request,'no_acces.html')
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

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

################## Relatório ####################

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
    STATUS_REGISTRO = Registro.STATUS_REGISTRO
    
    for i in STATUS_REGISTRO:
        registros.append(obj(i[0],Registro.objects.filter(status=i[0]).count))
    dados = {
        'dados':registros
    }
    return render(request,'report.html', dados)

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('account_login'))
    if request.user.is_superuser:
        registros = Registro.objects.all()
    else:
        registros = Registro.objects.filter(user_id=request.user.id)
    registros.order_by('id')
    context = {
        'registros': registros
    }
    return render(request,'dashboard.html', context=context)


# Fim views


def erro_404(request):
    print('--------------------------------')
    #h = list(User.objects.filter(id=1).values())[0]['username']

    print('---------------------------------')
    return render(request,'404.html')