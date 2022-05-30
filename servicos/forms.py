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
        fields = '__all__'

    def clean_patrimonio(self):
        key = self.cleaned_data['patrimonio']

        if models.Registro.objects.filter(patrimonio=key).exclude(status='Finalizado').exclude(status='Cancelado'):
            raise ValidationError(_('Invalid date - renewal in past'))
        return key