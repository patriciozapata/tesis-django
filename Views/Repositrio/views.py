from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from foro.forms import DocumentosForm,TipoForm
from .models import *
from cuentas.models import User
from .models import *
import datetime # horario
from django.utils import timezone #fecha 2018-11-29
from django.core.paginator import Paginator
from django.contrib import messages # MENSAJE
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views import View

# Create your views here.


class ViewRepositorio(View):
    template_name='repositorio/Visualizararchivos.html'
    def get(self,request):
        documentos = Documentos.objects.all().order_by('id')
        userx = User.objects.get (pk = request.user.id)
        notifications = userx.notifications.exclude(actor_object_id=request.user.id)
        paginator = Paginator(documentos, 5)
        page = request.GET.get('page')
        documentos = paginator.get_page(page)
        context = {
            'documentos':documentos,
            'notifications':notifications,
            'unread_count': userx.notifications.unread().count(),
        }
        return render(request, self.template_name, context)
    def post(self,request,test):
        test = request.POST['buscalo']
        queryset = Documentos.objects.filter(nombre = test)
        userx = User.objects.get (pk = request.user.id)
        notifications = userx.notifications.exclude(actor_object_id=request.user.id)
        documentos = Documentos.objects.all()
        paginator = Paginator(documentos, 3)
        page = request.GET.get('page')
        #?page=2
        documentos = paginator.get_page(page)
        context = {
            "object_list": queryset,
            'documentos':documentos,
            'notifications':notifications,
            'unread_count': userx.notifications.unread().count(),
        }
        return render(request, self.template_name,context)

class ViewVisualizarTesisParaPDF(ViewRepositorio):
    template_name= 'repositorio/visualizartesisnavegador.html'
    def get(self,request,pk):
        documentos = Documentos.objects.get(pk=pk)
        context = {
            'documentos':documentos,
        }
        return render (request, self.template_name,context)

class ViewVisualizarUnaTesis(ViewRepositorio):
    template_name='repositorio/Visualizartesis.html'
    def get(self,request,pk):
        documentos = Documentos.objects.get(pk=pk)
        tipo = Tipo.objects.get(pk=documentos.tipo_id)
        context = {
            'tipo':tipo,
            'documentos':documentos,
        }
        return render (request, self.template_name,context)

class ViewGuardarTesis(View):
    template_name='repositorio/GuardarArchivos.html'
    form = DocumentosForm()
    def get(self,request):
        return render(request,self.template_name,{'form':self.form})
    def post(self,request):
        form = DocumentosForm(request.POST, request.FILES)
        tipo2 = request.POST['tipo']
        tipo =  Tipo.objects.get(id= tipo2)
        documentos = Documentos.objects.all()
        if form.is_valid():
            time = timezone.now()
            form = Documentos(nombre = request.POST['nombre'],autor = request.POST['autor'],tipo = tipo,fecha=time,resumen = request.POST['resumen'],docfile = request.FILES['docfile'])
            form.save()
            messages.success(request,'registrado correctamente')
        return render (request,self.template_name,{'form':self.form})

class ViewFiltroDeTesisNombre(View):
    template_name='repositorio/filtronombre.html'
    def get(self,request):
        documentos = Documentos.objects.all().order_by('nombre')
        paginator = Paginator(documentos, 3)
        page = request.GET.get('page')
        documentos = paginator.get_page(page)
        context = {
            'documentos':documentos,
        }
        return render (request, self.template_name,context)

class ViewFiltroDeTesisAutor(ViewFiltroDeTesisNombre):
    template_name='repositorio/filtroautor.html'
    def get(self,request):
        documentos = Documentos.objects.all().order_by('autor')
        paginator = Paginator(documentos, 3)
        page = request.GET.get('page')
        documentos = paginator.get_page(page)
        context = {
            'documentos':documentos,
        }
        return render (request, self.template_name,context)

class ViewFiltroDeTesisFecha(ViewFiltroDeTesisNombre):
    template_name='repositorio/filtrofecha.html'
    def get(self,request):
        documentos = Documentos.objects.all().order_by('fecha')
        paginator = Paginator(documentos, 3)
        page = request.GET.get('page')
        documentos = paginator.get_page(page)
        context = {
            'documentos':documentos,
        }
        return render (request, self.template_name,context)

class ViewVisualizarCategoriasTesisPaneladmin(ViewFiltroDeTesisNombre):
    template_name= 'repositorio/visualizarcategoriastesis.html'
    def get(self,request):
        tipo = Tipo.objects.all()
        context = {
            "tipo": tipo,
        }
        return render (request, self.template_name,context)

class ViewBuscarporPost(View):
    template_name='repositorio/filtrototal.html'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        test = request.POST['buscalo']
        documentos = Documentos.objects.all()
        try:
            queryset = Documentos.objects.filter(Q(autor__istartswith=test)|Q(nombre__istartswith=test)|Q(resumen__istartswith=test))
        except  queryset.DoesNotExist:
            queryset = None
        context = {
            "object_list": queryset,
            'documentos':documentos,
        }
        return render(request, 'repositorio/filtrototal.html',context)

class ViewModificarTesis(View):
    template_name='repositorio/GuardarArchivos.html'
    def get(self,request,pk):
        documentos = get_object_or_404(Documentos, id=pk)
        form = DocumentosForm(instance=documentos)
        return render(request,self.template_name,{'form':form})
    def post(self,request,pk, *args, **kwargs):
        traedocumento =  Documentos.objects.get(id=pk)
        categorizaciontesis = request.POST['tipo']
        categorizaciontesis =  Tipo.objects.get(id= categorizaciontesis)
        time = timezone.now()
        archivo = request.POST['docfile']

        if archivo == 'null':
            documentos = Documentos(id=pk,nombre = request.POST['nombre'],autor = request.POST['autor'],tipo = categorizaciontesis,fecha=time,resumen = request.POST['resumen'],docfile = request.FILES['docfile'])
        else:
            documentos = Documentos(id=pk,nombre = request.POST['nombre'],autor = request.POST['autor'],tipo = categorizaciontesis,fecha=time,resumen = request.POST['resumen'],docfile = traedocumento.docfile)
        form = DocumentosForm(request.POST or None, request.FILES or None,instance=documentos)
        if form.is_valid():
            form.save()
            messages.success(request,'Modificado correctamente')
        return render (request,self.template_name, {'form': form})

class ViewEliminarTesis(View):
    template_name='repositorio/eliminartipos.html'
    def get(self,request,pk):
        documentos = Documentos.objects.get(id=pk)
        return render(request,self.template_name,{'documentos':documentos})
    def post(self,request,pk):
        documentos = Documentos.objects.get(id=pk)
        documentos.delete()
        messages.success(request,'registrado correctamente')
        return redirect('repositorio:Repositorio')

class ViewEliminarTipoTesis(View):
    template_name='repositorio/eliminarcategoriastesis.html'
    def get(self,request,pk):
        tipo = Tipo.objects.get(id=pk)
        return render(request,self.template_name,{'tipo':tipo})
    def post(self,request,pk):
        tipo = Tipo.objects.get(id=pk)
        tipo.delete()
        messages.success(request,'Se a eliminado correctamnte ')
        return redirect('repositorio:visualizarcategoriasdetesispaneladmin')

class ViewRegistroCategoriaTesis(View):
    template_name='repositorio/registrocategoriastesis.html'
    form = TipoForm()
    def get(self,request):
        return render(request,self.template_name,{'form':self.form})
    def post(self,request):
        form = TipoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'registrado correctamente')
        return render (request, 'repositorio/registrocategoriastesis.html',{'form':form})

class ViewModificarCategoriaTesis(View):
    template_name='repositorio/registrocategoriastesis.html'
    def get(self,request,pk, *args, **kwargs):
        tipo = get_object_or_404(Tipo, id=pk)
        form = TipoForm(instance=tipo)
        return render(request,self.template_name,{'form':form})
    def post(self,request,pk, *args, **kwargs):
        tipo = Tipo(id=pk,nombre = request.POST['nombre'])
        form = TipoForm(request.POST,instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request,'Modificado correctamente')
        return render (request,self.template_name,{'form':form})
