from django import forms

class FormularioConversor(forms.Form):
    Achatamiento = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    Parametro_A = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    Parametro_B = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    
