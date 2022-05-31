from dataclasses import field, fields
import django
from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = models.Departamento
        fields = "__all__"

class UnidadeForm(forms.ModelForm):
    class Meta:
        model = models.Unidade
        fields = "__all__"

class RegistroForm(forms.ModelForm):
    #patrimonio = forms.CharField(validators=[validarPatrimonio])
    class Meta:
        model = models.Registro
        fields = ['titulo','descricao','departamento_id','patrimonio','user']

    def clean_patrimonio(self, *args, **kwargs):
        key = self.cleaned_data.get('patrimonio')

        if models.Registro.objects.filter(patrimonio=key).exclude(status='Finalizado').exclude(status='Cancelado'):
            raise forms.ValidationError('Já existe um chamado para esse patrimonio!')
        else:
            return key