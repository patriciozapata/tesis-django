from django.shortcuts import render, redirect,render_to_response
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import  AuthenticationForm
from foro.forms import TopicoForm, Postform, ComentarioForm, Categoriaform, UserForm, PerfilForm,ModificarUserForm,ModificarDatosUserForm,DocumentosForm
from .models import *
from repositorio.models import Tipo,Documentos
from cuentas.models import User,Perfil
from django.core.paginator import Paginator
from django.views.decorators.csrf import  csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages # MENSAJE
from markdown import markdown# text de comentario
from django.utils import timezone #fecha 2018-11-29
from notifications.signals import notify
from notifications.models import Notification
from django.db.models import Q
from django.http import Http404
from django.views import View




class ViewUsuario(View):
    template_name = 'foro/principal.html'
    formulario = AuthenticationForm()
    def get(self, request):
        return render(request, self.template_name, {'form': self.formulario})
    def post(self, request):
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.get_user()
            login(request,user)
            return redirect('foro:Bienvenido')
        else:
            return render(request, 'foro/principal.html', {'form':formulario})


@csrf_exempt
def logout(request):
    logout(request)

class ViewVistaAdministrador(View):
    template_name= 'foro/administrador.html'
    def get(self,request):
        return render (request, self.template_name)

class ViewVisualizarUser(View):
    template_name= 'foro/visualizaruser.html'
    def get(self,request):
        queryset = User.objects.filter(admin=False)
        context = {
            "object_list": queryset,
        }
        return render(request, self.template_name,context)

class ViewVisualizarPerfiles(ViewVisualizarUser):
    template_name= 'foro/visualizarperfiles.html'
    def get(self,request):
        queryset = Perfil.objects.all()
        context = {
            "object_list": queryset,
        }
        return render(request, self.template_name,context)

class ViewVisualizarAdministradores(ViewVisualizarUser):
    template_name= 'foro/visualizaradministrador.html'
    def get(self,request):
        queryset = User.objects.filter(admin=True)
        context = {
            "object_list": queryset,
        }
        return render(request, self.template_name,context)

class ViewBuscarAdministradores(ViewVisualizarUser):
    template_name= 'foro/visualizaradministrador.html'
    def post(self,request):
        test = request.POST['buscalo']
        queryset = User.objects.filter(admin=True)
        querysetnombre = User.objects.filter(Q(nombre__istartswith=test),admin=True)
        context = {
            "object_list": queryset,
            "informacion": querysetnombre,
        }
        return render(request, self.template_name,context)

class ViewBuscarUser(ViewVisualizarUser):
    template_name= 'foro/visualizaruser.html'
    def post(self,request):
        test = request.POST['buscalo']
        queryset = User.objects.filter(staff=False)
        querysetnombre = User.objects.filter(Q(nombre__istartswith=test),admin=False,staff=False)
        context = {
            "object_list": queryset,
            "object_lists": querysetnombre,
        }
        return render(request, self.template_name,context)

class ViewEliminarUser(ViewVisualizarUser):
    template_name='foro/eliminaruserr.html'
    def get(self,request,username):
        user = User.objects.get(email=username)
        notifications = Notification.objects.filter(actor_object_id=user.id)
        return render(request,self.template_name,{'user':user})
    def post(self,request,username):
        user = User.objects.get(email=username)
        notifications = Notification.objects.filter(actor_object_id=user.id)
        user.delete()
        notifications.delete()
        queryset = User.objects.filter(staff=False)
        context = {
            "object_list": queryset,
        }
        return render (request, 'foro/visualizaruser.html',context)

class ViewRegistroPerfilesUser(View):
    template_name='foro/registrodeperfil.html'
    form = PerfilForm()
    def get(self,request):
        return render(request,self.template_name,{'form':self.form})
    def post(self,request):
        form = PerfilForm(request.POST)
        if form.is_valid():
            messages.success(request,'registrado correctamente')
            form.save()
        return render (request,self.template_name,{'form':form})

class ViewRegistroUser(View):
    template_name='foro/registrouser.html'
    form = UserForm()
    def get(self,request):
        return render(request,self.template_name,{'form':self.form})
    def post(self,request):
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            datos = form.cleaned_data
            perfil = Perfil.objects.get(perfil=datos['perfil'])
            test = datos['perfil']
            DirectorCarreara = Perfil.objects.get(perfil='Director de carrera')
            Coordinador = Perfil.objects.get(perfil='Coordinador')
            CoordinadorEspecializado = Perfil.objects.get(perfil='Coordinador Especializado')
            imagen2 = datos['imagen']
            if (test == DirectorCarreara ):
                usuario = User.objects.create_superuser(datos['email'],datos['nombre'],datos['apellido'],DirectorCarreara.id, True ,True,datos['password'])
                usuario.imagen = imagen2
                usuario.save()
                messages.success(request,'registrado correctamente ')
            elif (test == Coordinador or test == CoordinadorEspecializado ):
                usuario = User.objects.create_superuser(datos['email'],datos['nombre'],datos['apellido'],Coordinador.id, True ,False,datos['password'])
                usuario.imagen = imagen2
                usuario.save()
                messages.success(request,'registrado correctamente ')
            else:
                usuario = User.objects.create_user(datos['email'],datos['nombre'],datos['apellido'], perfil.id, datos['password'])
                usuario.imagen = imagen2
                usuario.save()
                messages.success(request,'registrado correctamente sin privilegios')
        return render (request,self.template_name,{'form':form})

class ViewModificarUser(View):
    template_name='foro/modificacionUser.html'
    def get(self,request,username, *args, **kwargs):
        user = get_object_or_404(User, email=username)
        form = ModificarDatosUserForm(instance=user)
        return render(request,self.template_name,{'form':form})
    def post(self,request,username, *args, **kwargs):
        user = get_object_or_404(User, email=username)
        form = ModificarDatosUserForm(request.POST, instance=user)
        if form.is_valid():
            datos = form.cleaned_data
            password = datos['password']
            imagen2 = datos['imagen']
            user.set_password(password)
            user.imagen = imagen2
            user.save()
            messages.success(request,'Se a modificado correctamente sus datos ')
        return render (request,self.template_name,{'form':form})

class ViewModificarPerfilesUser(View):
    template_name='foro/registrodeperfil.html'
    def get(self,request,pk, *args, **kwargs):
        perfil = get_object_or_404(Perfil, id=pk)
        form = PerfilForm(instance=perfil)
        return render(request,self.template_name,{'form':form})
    def post(self,request,pk, *args, **kwargs):
        perfil = get_object_or_404(Perfil, id=pk)
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            messages.success(request,'Se a modificado correctamente sus datos ')
            perfil.save()
        return render (request,self.template_name,{'form':form})

class ViewEliminarPerfilUser(View):
    template_name='foro/eliminarperfil.html'
    def get(self,request,pk):
        perfil = Perfil.objects.get(id=pk)
        return render(request,self.template_name,{'perfil':perfil})
    def post(self,request,pk):
        perfil = Perfil.objects.get(id=pk)
        perfil.delete()
        messages.success(request,'Se a eliminado correctamnte ')
        return redirect('foro:visualizarperfils')

class ViewForoBienvenido(View):
    template_name= 'foro/bienvenido.html'
    def get(self,request):
        topico = Topico.objects.all().order_by('id')
        user = request.user
        userr = User.objects.get(email=user)
        userx = User.objects.get (pk = userr.id)
        notifications = userx.notifications.exclude(actor_object_id=userr.id)
        context = {
            'topico': topico,
            'notifications':notifications,
            'unread_count': userx.notifications.unread().count(),
        }
        paginator = Paginator(topico, 3)
        page = request.GET.get('page')
        topico = paginator.get_page(page)
        return render(request,self.template_name, context)

class ViewListarTopicos(View):
    template_name= 'foro/editar.html'
    def get(self,request):
        topico = Topico.objects.all().order_by('id')
        paginator = Paginator(topico, 3)
        page = request.GET.get('page')
        topico = paginator.get_page(page)
        return render(request,self.template_name,{'topico': topico})

class ViewRegistroTopico(View):
    template_name='foro/registrotopico.html'
    form = TopicoForm()
    def get(self,request):
        return render(request,self.template_name,{'form':self.form})
    def post(self,request):
        form = TopicoForm(request.POST)
        if form.is_valid():
            messages.success(request,'Se a modificado correctamente sus datos ')
            form.save()
        return render (request,self.template_name,{'form':form})

class ViewVerListaPost(View):
    template_name='foro/listadoPost.html'
    def get(self,request,pk):
        post = Post.objects.filter(categoria_id=pk)
        categoria = Categoria.objects.get(id=pk)
        respuesta = Post.objects.filter(categoria_id=pk).count()
        paginator = Paginator(post, 20)
        page = request.GET.get('page')
        post = paginator.get_page(page)
        context = {
            'post':post,
            'categoria':categoria,
        }
        return render(request,self.template_name,context)

class ViewRegistroTemaEnPost(View):
    template_name= 'foro/RegistroUnoPost.html'
    def get(self,request,pk):
        form = Postform()
        categoria = Categoria.objects.get(pk=pk)
        context = {
            'form':form,
            'categoria':categoria,
        }
        return render(request,self.template_name,context)
    def post(self,request,pk):
        time = timezone.now()
        usuariologeado= request.user
        usuarioadministrado = User.objects.filter(staff=True)
        post = Post(categoria_id=pk, user=request.user ,fecha =time)
        informaciontema= Categoria.objects.get(id=pk)
        form = Postform(request.POST, instance=post)
        categoria = Categoria.objects.get(id=pk)
        if form.is_valid():
            datos = form.cleaned_data
            id = datos['titulo']
            temaid=pk
            messages.success(request,'registrado correctamente')
            notify.send(usuariologeado, recipient=usuarioadministrado,target_object_id=categoria.topico_id, verb='Se a creado un nuevo tema discusion',nivel='info',action=informaciontema.id,action_object=informaciontema,target=post,description=id,timestamp=timezone.now())
            form.save()
            categoria = Categoria.objects.get(pk=pk)
            context = {
                'form':form,
                'categoria':categoria,
            }
        return render (request, self.template_name,context)

class ViewRegistrarLike(View):
    def post(self,request):
        comentario = request.POST.get('idComentario')
        comentario = Comentario.objects.get(pk=comentario)
        user = request.user
        user = User.objects.get(email=user)
        like = Like.objects.filter(comentario=comentario, user=user)
        if like.exists() == False:
            like = Like(comentario=comentario, user=user)
            like.save()
            reg = True
        else:
            like.delete()
            reg = False
        return HttpResponse(reg)

class ViewEliminarLike(View):
    def post(self,request):
        comentarioid = request.POST.get('comentarioid')
        print(comentarioid)
        user = request.user
        like = Like.objects.filter(comentario_id=comentarioid)
        like.delete()
        like = Like.objects.filter(comentario_id=comentarioid).count()
        print(like)
        return HttpResponse(like)
# BUG: like
class ViewRegistroCategoriaTopico(View):
    template_name='foro/registrocategoria.html'
    form = Categoriaform()
    def get(self,request):
        return render(request,self.template_name,{'form':self.form})
    def post(self,request):
        form = Categoriaform(request.POST)
        if form.is_valid():
            messages.success(request,'Se a modificado correctamente sus datos ')
            form.save()
        return render (request,self.template_name,{'form':form})

class ViewTemasDiscusion(View):
    template_name= 'foro/comentarios.html'
    def get(self,request,pk):
        comentario = Comentario.objects.filter(post_id=pk).order_by('id')
        user = request.user
        userr = User.objects.get(email=user)
        post = Post.objects.get(id=pk)
        categoria =Categoria.objects.get(id=post.categoria_id)
        paginator = Paginator(comentario, 20)
        like = Like.objects.filter(user_id=userr.id)
        page = request.GET.get('page')
        comentario = paginator.get_page(page)
        form =ComentarioForm()
        context = {
            'comentario':comentario,
            'post':post,
            'like':like,
            'categoria':categoria,
            'form':form,
        }
        visitas = Visitas.objects.create(visita=True , post_id=post.id, user=userr)
        return render (request,self.template_name,context)
    def post(self,request,pk):
        hola = request.user
        time = timezone.now()
        posteo= Post.objects.get(id=pk)
        post1 = Comentario(post_id=pk, fecha=time,user=request.user)
        usuario = Post.objects.get(id=pk)
        print(usuario)
        usuariox= User.objects.get(id=usuario.user_id)
        form = ComentarioForm(request.POST, instance=post1)
        if form.is_valid():
            datos = form.cleaned_data
            id = datos['comentario']
            notify.send(hola, recipient=usuariox, verb='Te comentaron',nivel='info',action=posteo.id,action_object=posteo,description=id,timestamp=timezone.now())
            messages.success(request,'Se a modificado correctamente sus datos ')
            form.save()
            postid= pk
        return redirect('foro:temadiscusion', pk=postid)
# BUG: comentarios
class ViewVerPerfil(View):
    template_name='foro/perfil.html'
    def get(self,request):
        queryset = User.objects.get(id=request.user.id)
        post = Post.objects.filter(user_id=queryset.id)
        comentario = Comentario.objects.filter(user_id=queryset.id)
        visita = Visitas.objects.filter(user_id=queryset.id)
        context = {
            "object_list": queryset,
            'post':post,
            'comentario':comentario,
            'visita':visita,
        }
        return render(request,self.template_name,context)

class ViewModificarMiUser(View):
    template_name='foro/modificaruser.html'
    def get(self,request,pk):
        user = get_object_or_404(User, id=pk)
        form = ModificarUserForm(instance=user)
        return render(request,self.template_name,{'form':form})
    def post(self,request,pk):
        user = get_object_or_404(User, id=pk)
        perfil = Perfil.objects.get(perfil=user.perfil)
        usariologeado = request.user
        user = User(id= pk,email=user.email,staff=user.staff,admin=user.admin,perfil=perfil)
        form = ModificarUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            datos = form.cleaned_data
            password = datos['password']
            imagen2 = datos['imagen']
            user.set_password(password)
            user.imagen = imagen2
            messages.success(request,'Se a modificado correctamente sus datos ')
            user.save()
        return render (request,self.template_name,{'form':form})

class ViewEditarTopico(View):
    def post(self,request):
        id = request.POST.get('id')
        nombre = request.POST.get('nombreTopico')
        topico = Topico.objects.get(pk=id)
        topico.nombre = nombre
        topico.save()
        return HttpResponse()# BUG: actulizar topico

class ViewEliminarTopico(View):
    def post(self,request):
        id = request.POST.get('id')
        nombre = request.POST.get('nombreTopico')
        topico = Topico.objects.get(pk=id)
        topico.nombre = nombre
        categoria = Categoria.objects.get(topico_id=id)
        notifications = Notification.objects.filter(action_object_object_id=categoria.topico_id)
        notifications.delete()
        topico.delete()
        return HttpResponse(nombre)# BUG: aeliminar de topico

class ViewEditarCategoriaTopico(View):
    def post(self,request):
        id = request.POST.get('id')
        nombre = request.POST.get('nombreTopico')
        categoria = Categoria.objects.get(pk=id)
        categoria.nombre = nombre
        categoria.save()
        return HttpResponse()

class ViewEliminarCategoriaTopico(View):
    def post(self,request):
        id = request.POST.get('id')
        nombre = request.POST.get('nombreTopico')
        categoria = Categoria.objects.get(pk=id)
        notifications = Notification.objects.filter(action_object_object_id=id)
        categoria.nombre = nombre
        notifications.delete()
        categoria.delete()
        return HttpResponse(nombre)
# BUG: Categorias
class ViewModificaPost(View):
    template_name='foro/RegistroUnoPost.html'
    def get(self,request,post):
        post = get_object_or_404(Post, id=post)
        form = Postform(instance=post)
        return render(request,self.template_name,{'form':form})
    def post(self,request,post):
        post = get_object_or_404(Post, id=post)
        time = timezone.now()
        post = Post( pk= post.id, categoria_id= post.categoria_id ,fecha=time, user=request.user)
        form = Postform(request.POST, instance=post)
        if form.is_valid():
            messages.success(request,'Se a modificado correctamente sus datos ')
            form.save()
        return render (request,self.template_name,{'form':form})

class ViewModificaComentario(View):
    template_name='foro/RegistroComentario.html'
    def get(self,request,pk):
        comentario = get_object_or_404(Comentario, id=pk)
        form = ComentarioForm(instance=comentario)
        return render(request,self.template_name,{'form':form})
    def post(self,request,pk):
        comentario = get_object_or_404(Comentario, id=pk)
        time = timezone.now()
        comentario = Comentario( pk= pk, post_id=comentario.post_id ,fecha=time, user=request.user)
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            messages.success(request,'Se a modificado correctamente sus datos ')
            form.save()
            postid= comentario.post_id
            return redirect('foro:temadiscusion', pk=postid)

class ViewEliminarPost(View):
    template_name= 'foro/post_eliminar.html'
    def get(self,request,post):
        post = Post.objects.get(id=post)
        return render(request,self.template_name,{'post':post})
    def post(self,request,post):
        post = Post.objects.get(id=post)
        notifications = Notification.objects.filter(description=post.titulo)
        notifications.delete()
        post.delete()
        messages.success(request,'Se a Eliminado correctamente el Tema de discusion ')
        return redirect('foro:mostrarListadoPost', pk=post.categoria_id)

class ViewEliminarComentario(View):
    template_name= 'foro/comentario_eliminar.html'
    def get(self,request,comentario):
        comentario = Comentario.objects.get(id=comentario)
        return render(request,self.template_name,{'comentario':comentario})
    def post(self,request,comentario):
        comentario = Comentario.objects.get(id=comentario)
        postid= comentario.post_id
        notifications = Notification.objects.filter(description=comentario.comentario)
        notifications.delete()
        comentario.delete()
        messages.success(request,'Se a Eliminado correctamente el Tema de discusion ')
        return redirect('foro:temadiscusion', pk=postid)

class ViewVisualizarNotificaciones(View):
    template_name= 'foro/Visualizarnotificaciones.html'
    def get(self,request):
        userx = User.objects.get(email=request.user)
        notifications = userx.notifications.exclude(actor_object_id=request.user.id).order_by('timestamp')
        context = {
            'notifications':notifications,
            'unread_count': userx.notifications.unread().count(),
        }
        return render(request,self.template_name,context)

class ViewRedireccionNotificacions(View):
    def get(self,request,id, informacion,pk):
        notifications = Notification.objects.get(description=informacion,action_object_object_id=pk,id=id)
        try:
            comentario = Comentario.objects.filter(post_id=notifications.action_object_object_id)
            notifications.unread=False
            notifications.save()
        except Comentario.DoesNotExist :
            comentario = None
        try:
            post = Post.objects.get(titulo=informacion)
            categoria = Categoria.objects.get(id=post.categoria_id)
            notifications.unread=False
            notifications.save()
        except Post.DoesNotExist or Categoria.DoesNotExist:
            post = None
            categoria = None
        if categoria == None:
            print("Nada")
        else:
            return redirect('foro:mostrarListadoPost', pk=categoria.id)
        if comentario == None:
            print("Nada")
        else:
            return redirect('foro:temadiscusion', pk=notifications.action_object_object_id)

from django.shortcuts import render
from django.http import HttpResponse


def error_404_view(request, exception):
    data = {"name": "informacion"}
    return render(request,'foro/404.html', data)


def error_500_view(request,exception):
        data = {"name": "informacion "}
        return render(request,'foro/500.html', data)
