from django import forms
from foro.models import *
from cuentas.models import User,Perfil
from repositorio.models import Tipo,Documentos
from .views import *
from django.utils.html import mark_safe
from django.utils.text import Truncator
from markdown import markdown

MARKDOWN = 'markdown'

class TopicoForm(forms.ModelForm):
    class Meta:
        model = Topico
        fields= [
            'nombre'
        ]
        labels = {
            'nombre':'Nombre del topico'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'})
        }

class Categoriaform(forms.ModelForm):
    class Meta:
        model = Categoria
        fields= [
            'topico',
            'nombre',
        ]
        labels = {
            'topico': 'Seleccione el topico',
            'nombre':'nombre',

        }
        widgets = {
            'topico': forms.Select(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
        }

class Postform(forms.ModelForm):
    class Meta:
        model = Post
        exclude=['user','categoria','fecha']
        fields= [
            'titulo',
            'descripcion',

        ]
        labels = {
            'titulo':'Ingrese el nombre del post',
            'descripcion':'Ingrese la descripcion del tema',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control','placeholder':'titulos'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control','placeholder':'descripcion'}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        exclude=['post','user','fecha']
        fields= [
            'comentario',
        ]
        labels = {
            'comentario':'Ingrese el nombre el comentario',
        }
        widgets = {
            'comentario': forms.Textarea(attrs={'class':'markdown','placeholder':'Ingrese su comentario'}),
        }


class UserForm(forms.ModelForm):
#    def __init__(self , *args, **kwargs):
#        super(UserForm, self).__init__(*args, **kwargs)
#        self.fields['perfil'].queryset =  Perfil.objects.filter(perfil='Admin')

    class Meta:
        model = User
        exclude=['staff']
        fields= [
            'email',
            'perfil',
            'nombre',
            'apellido',
            'imagen',
            'password',
        ]
        labels = {
            'email':'Ingrese su email:',
            'perfil': 'Seleccione el perfil',

            'nombre':'Ingrese su nombre',
            'apellido':'Ingrese su apellido',
            'imagen':'Ingrese su imagen de usuario',
            'password':'Ingrese su contraseña',
        }
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'perfil':forms.Select(attrs={'class':'form-control','placeholder':'email'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
            'apellido':forms.TextInput(attrs={'class':'form-control','placeholder':'apellido'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'password','type':'password'}),
        }

class ModificarDatosUserForm(forms.ModelForm):
#    def __init__(self , *args, **kwargs):
#        super(UserForm, self).__init__(*args, **kwargs)
#        self.fields['perfil'].queryset =  Perfil.objects.filter(perfil='Admin')
    class Meta:
        model = User
        exclude=['admin']
        fields= [
            'email',
            'perfil',
            'staff',
            'nombre',
            'apellido',
            'imagen',
            'password',
            'is_active',
        ]
        labels = {
            'email':'Ingrese su email:',
            'perfil': 'Seleccione el perfil',
            'staff':'Desea Privilegios de staff',
            'nombre':'Ingrese su nombre',
            'apellido':'Ingrese su apellido',
            'imagen':'Ingrese su imagen de usuario',
            'password':'Ingrese su contraseña',
            'is_active':'Desea bloquear la cuenta',
        }
        widgets = {
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'email'}),
            'perfil':forms.Select(attrs={'class':'form-control','placeholder':'perfil'}),
            'admin':forms.CheckboxInput(),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
            'apellido':forms.TextInput(attrs={'class':'form-control','placeholder':'apellido'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'password','type':'password'}),
        }
        def clean(self):
            super(ModificarDatosUserForm, self).clean() #if necessary
            if self.cleaned_data.get('email') in self._errors:
                del self._errors['email']
            return self.cleaned_data


class ModificarUserForm(forms.ModelForm):
#    def __init__(self , *args, **kwargs):
#        super(UserForm, self).__init__(*args, **kwargs)
#        self.fields['perfil'].queryset =  Perfil.objects.filter(perfil='Admin')

    class Meta:
        model = User
        exclude=['staff','admin','perfil','email']
        fields= [
            'nombre',
            'apellido',
            'imagen',
            'password',
        ]
        labels = {
            'nombre':'Ingrese su nombre',
            'apellido':'Ingrese su apellido',
            'imagen':'Ingrese su imagen de usuario',
            'password':'Ingrese su contraseña',
        }
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
            'apellido':forms.TextInput(attrs={'class':'form-control','placeholder':'apellido'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'password','type':'password'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields= [
            'id',
            'perfil',

        ]
        labels = {
            'id':'Ingrese un numero para asignarle el perfil',
            'perfil': 'Seleccione el perfil',

        }
        widgets = {
            'id': forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingrese un numero '}),
            'perfil': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el nombre del perfil'}),
        }

class DocumentosForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(DocumentosForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['docfile'].required = False

    class Meta:
        model = Documentos
        fields= [
            'nombre',
            'autor',
            'tipo',
            'resumen',
            'docfile',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese un Titulo'}),
            'autor': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el nombre autor'}),
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'resumen': forms.Textarea(attrs={'class':'form-control','placeholder':'Ingrese el resumen'}),
        }


class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields= [
            'nombre',
        ]
        labels = {
            'nombre':'Ingrese el Categoria',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese la categorias  que estara con la tesis '}),
        }
