from django.db import models
from datetime import date


class Unidade(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Departamento(models.Model):
    nome = models.CharField(max_length=50)
    unidade_id = models.ForeignKey(Unidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Registro(models.Model):

    STATUS_REGISTRO = (
        ('Pendente', 'Pendente'),
        ('Em andamento', 'Em andamento'),
        ('Finalizado', 'Finalizado'),
        ('Cancelado', 'Cancelado')
    )

    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True, max_length=200)
    criado_em = models.DateField(default = date.today)
    departamento_id = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_REGISTRO)
    #finalizado_em = models.DateField(default=)
    patrimonio = models.CharField(max_length=10, unique=True)


    def __str__(self):
        return self.titulo


