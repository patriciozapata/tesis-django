from django.conf.urls import url, include
from .views import *
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.views import logout
import notifications.urls


app_name='foro'

from django.conf.urls import (
handler400, handler403, handler404, handler500
)


urlpatterns = [
    url(r'^$', ViewUsuario.as_view(), name="ingresar"),
    url(r'^foro/administrador/visualizaruser$', login_required(ViewVisualizarUser.as_view()), name="visualizaruser"),
    url(r'^foro/perfil/visualozarperfiles/$', login_required(ViewVisualizarPerfiles.as_view()), name="visualizarperfils"),
    url(r'^foro/administrador/visualizaradministrador$', login_required(ViewVisualizarAdministradores.as_view()), name="visualizaradministrador"),
    url(r'^foro/administrador/visualizaradministrador/$', login_required(ViewBuscarAdministradores.as_view()), name="buscaradministradores"),
    url(r'^foro/administrador/visualizaruser/$', login_required(ViewBuscarUser.as_view()), name="busquedauserr"),
    url(r'^foro/administrador/visualizaruser/eliminaruser/(?P<username>[\w.@+-]+)/$', login_required(ViewEliminarUser.as_view()), name="eliminaruser"),
    url(r'^foro/administrador/$', login_required(ViewVistaAdministrador.as_view()), name="administradorr"),
    url(r'^foro/administrador/registrodeperfiles/$', login_required(ViewRegistroPerfilesUser.as_view()), name="registrodeperfile"),

    url(r'^Bienvenido/$', login_required(ViewForoBienvenido.as_view()), name="Bienvenido"),

    url(r'^Temas_Discusion/(?P<pk>\d+)/$', login_required(ViewVerListaPost.as_view()), name="mostrarListadoPost"),

    url(r'^perfil/', login_required(ViewVerPerfil.as_view()), name="perfil"),

    url(r'^registrotopico/', login_required(ViewRegistroTopico.as_view()), name="registro"),
    url(r'^Editar/', login_required(ViewListarTopicos.as_view()), name="Editar"),

    url(r'^ingresartemas/(?P<pk>\d+)$', login_required(ViewRegistroTemaEnPost.as_view()), name="ingresartemas"),

    url(r'^actualizarCategoria/$', login_required(ViewEditarCategoriaTopico.as_view()), name="actualizarCategoria"),
    url(r'^eliminarCategoria/$', login_required(ViewEliminarCategoriaTopico.as_view()), name="eliminarCategoria"),
    url(r'^agregarcategoria/$', login_required(ViewRegistroCategoriaTopico.as_view()), name="agregarcategoria"),

    url(r'^post/(?P<pk>\d+)$', login_required(ViewTemasDiscusion.as_view()), name="temadiscusion"),
    url(r'^editarcomentario/(?P<pk>\d+)$', login_required(ViewModificaComentario.as_view()), name="editarcomentario"),
    url(r'^eliminarcomentario/(?P<comentario>\d+)$', login_required(ViewEliminarComentario.as_view()), name="eliminarcomentario"),

    url(r'^actualizar/$', login_required(ViewEditarTopico.as_view()), name="actualizar"),
    url(r'^eliminar/$', login_required(ViewEliminarTopico.as_view()), name="eliminar"),

    url(r'^eliminar_post/(?P<post>\d+)$', login_required(ViewEliminarPost.as_view()), name="eliminarpost"),
    url(r'^Temas_Discusion/comentario/editarpost/(?P<post>\d+)$', login_required(ViewModificaPost.as_view()), name="editarpost"),

    url(r'^registrolike/', login_required(ViewRegistrarLike.as_view()), name="registrolike"),
    url(r'^eliminarlike/', login_required(ViewEliminarLike.as_view()), name="eliminarlike"),

    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),









    url(r'^foro/createuser/registrouser/$', login_required(ViewRegistroUser.as_view()), name="registrouser"),


    url(r'^foro/administrador/editarperfiles/(?P<pk>\d+)/$', login_required(ViewModificarPerfilesUser.as_view()), name="editarperfiles"),

    url(r'^foro/perfil/modificaruser/(?P<pk>\d+)/$', login_required(ViewModificarMiUser.as_view()), name="modificardatosuser"),
    url(r'^foro/perfil/modificardatosuser/(?P<username>[\w.@+-]+)/$', login_required(ViewModificarUser.as_view()), name="modificadouser"),

    url(r'^foro/perfil/eliminarperfile/(?P<pk>\d+)/$', login_required(ViewEliminarPerfilUser.as_view()), name="eliminarperfiles"),

    url(r'^', include('notifications.urls', namespace='notifications')),
    url(r'^foro/bienvenido/notificacionesredirrecionamiento/(?P<id>\d+)/(?P<informacion>[\w ]+)/(?P<pk>\d+)//$', login_required(ViewRedireccionNotificacions.as_view()), name="Notificacionesredirrecionamiento"),
    url(r'^foro/Bienvenido/Visualizarnotificaciones/$', ViewVisualizarNotificaciones.as_view(), name="visualizarnotificaciones"),




]
