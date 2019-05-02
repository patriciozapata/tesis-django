from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import login_required

app_name='repositorio'



urlpatterns = [
        url(r'^$', login_required(ViewRepositorio.as_view()), name="Repositorio"),
        url(r'^repositorio/Visualizararchivos/tesis/Visualizararchivospdf/(?P<pk>\d+)$', login_required(ViewVisualizarTesisParaPDF.as_view()), name="Visualizararchivospdf"),
        url(r'^repositorio/Visualizararchivos/tesis/visualizarcategoriasdetesispaneladmin$', login_required(ViewVisualizarCategoriasTesisPaneladmin.as_view()), name="visualizarcategoriasdetesispaneladmin"),
        url(r'^repositorio/Visualizararchivos/tesis/(?P<pk>\d+)$', login_required(ViewVisualizarUnaTesis.as_view()), name="Visualizartesis"),
        url(r'^repositorio/GuardarArchivos/$', login_required(ViewGuardarTesis.as_view()), name="GuardarArchivos"),
        url(r'^repositorio/Visualizararchivos/tesis/filtro$', login_required(ViewFiltroDeTesisFecha.as_view()), name="filtro"),
        url(r'^repositorio/Visualizararchivos/tesis/filtroautor$', login_required(ViewFiltroDeTesisAutor.as_view()), name="filtroautor"),
        url(r'^repositorio/Visualizararchivos/tesis/filtronombre$', login_required(ViewFiltroDeTesisNombre.as_view()), name="filtronombre"),
        url(r'^repositorio/Visualizararchivos/tesis/buscadortotal$', login_required(ViewBuscarporPost.as_view()), name="buscadortota"),
        url(r'^repositorio/Visualizararchivos/tesis/modificaciontesis/(?P<pk>\d+)$', login_required(ViewModificarTesis.as_view()), name="modificaciontesi"),
        url(r'^repositorio/Visualizararchivos/tesis/eliminartesis/(?P<pk>\d+)$', login_required(ViewEliminarTesis.as_view()), name="eliminartesi"),
        url(r'^repositorio/registrocategoriastesis/$',  login_required(ViewRegistroCategoriaTesis.as_view()), name="registrocategoriastesis"),
        url(r'^repositorio/eliminartipotesis/(?P<pk>\d+)$', login_required(ViewEliminarTipoTesis.as_view()), name="eliminartipotesis"),
        url(r'^repositorio/modificarcategoriastesis/(?P<pk>\d+)$', login_required(ViewModificarCategoriaTesis.as_view()), name="modificarcategoriastesis"),
]
