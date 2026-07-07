from django import forms
from .models import Projeto, Tecnologia, Competencia, Formacao
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistoForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'

class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = '__all__'

class FormacaoForm(forms.ModelForm):
    class Meta:
        model = Formacao
        fields = '__all__'

class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = Competencia
        fields = '__all__'