from django.conf.urls import url, include
from . import views

app_name='carto'
urlpatterns = [
    url(r'^$', views.mapa, name="Mapa"),
    url(r'^Test$', views.mapaPato, name="MapaPato"),
    url(r'^Data/(?P<idMapa>\d+)/$', views.loadPoligonos, name="Data"),
    url(r'^DataAll/(?P<idMapa>\d+)/$', views.loadAll, name="DataAll"),
    url(r'^Puntos/(?P<idMapa>\d+)/$', views.loadPuntos, name="Puntos"),
    url(r'^Lineas/(?P<idMapa>\d+)/$', views.loadLineas, name="Lineas"),
    url(r'^Poligonos/(?P<idMapa>\d+)/$', views.loadPoligonos, name="Poligonos"),
    url(r'^nuevoMapa$', views.crearNuevoMapa, name="nuevoMapa"),
    url(r'^eliminarMapa$', views.eliminarMapa, name="eliminarMapa"),
    url(r'^updateNP$', views.actualizarNombreMapa, name="updateNP"),
    url(r'^updateNG$', views.actualizarNombreGeometria, name="updateNG"),
    url(r'^actualizar$', views.actualizar, name="actualizar"),
    url(r'^insertar$', views.insertar, name="insertar"),
    url(r'^eliminar$', views.eliminar, name="eliminar")
]
