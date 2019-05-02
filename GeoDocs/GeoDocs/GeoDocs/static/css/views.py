from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from foro.forms import TopicoForm,TemasForm
from .models import *
from conversor.forms import FormularioConversor
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json, math


@csrf_exempt
def principal(request):
    return render(request,'foro/principal.html')
def cargarforo(request):
    return render(request,'topicos/topicos.html')

@csrf_exempt
def ingresar (request):
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.get_user()
            login(request,user)
            return redirect('foro:Bienvenido')
            #return HttpResponseRedirect(reverse('foro:Bienvenido'), request)
    else:
        formulario = AuthenticationForm()
    return render(request, 'foro/principal.html', {'form':formulario})


#Topicos vista 2
def topico(request):
    return render (request, 'topicos/topicos.html')
def registroTopico(request):
    if request.method == 'POST':
        form = TopicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('foro:Bienvenido')
    else:
        form = TopicoForm()
    return render (request, 'foro/registrotopico.html',{'form':form})

def listarTopico(request):
    topico = Topico.objects.all().order_by('id')
    for temp in topico:
        print(temp.nombre)
        for categoria in temp.categoria_set.all().order_by('id'):
            print(categoria.nombre)
    context = {'topico':topico}
    temp = request.path
    if(temp == '/foro/topico/'):
        return render(request,'foro/topicos.html',context)
    else:
        return render(request,'foro/Editar.html',context)


@csrf_exempt
def mostrarPost(request):
    #val idCategoria = request.POST.get('idCategoria')
    #listaPost = Entrada.objects.get(categoria=idCategoria).order_by('id')
    #context = {'lstPost':listaPost}
    return render (request, 'foro/listadoPost.html')
def ingresartemas(request):
    if request.method == 'POST':
        form = TemasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('foro')
    else:
        form =TemasForm()
    return render (request, 'foro/registropost.html',{'form':form})

def comentario(request):
    return render (request, 'foro/comentarios.html')

def perfil(request):
    return render (request, 'foro/perfil.html')


def repositorio(request):
    return render (request, 'repositorio/Archivossubidos.html')


def actualizar(request):
    id = request.POST.get('id')
    nombre = request.POST.get('nombreTopico')
    topico = Topico.objects.get(pk=id)
    topico.nombre = nombre
    topico.save()
    return HttpResponse(nombre)


def eliminar(request):
    id = request.POST.get('id')
    nombre = request.POST.get('nombreTopico')
    topico = Topico.objects.get(pk=id)
    topico.nombre = nombre
    topico.delete()
    return HttpResponse(nombre)
