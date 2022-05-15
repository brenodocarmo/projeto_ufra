from dataclasses import field, fields
from django.forms import ModelForm
from . import models

class DepartamentoForm(ModelForm):
    class Meta:
        model = models.Departamento
        fields = "__all__"

class UnidadeForm(ModelForm):
    class Meta:
        model = models.Unidade
        fields = "__all__"

class RegistroForm(ModelForm):
    class Meta:
        model = models.Registro
        fields = "__all__"