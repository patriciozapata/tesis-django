from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from .models import Mapa, Poligono, Punto, CadenaLinea
from cuentas.models import User
from carto.forms import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.gis.geos import GEOSGeometry

@ensure_csrf_cookie
def mapa(request):
    usuario = request.user
    usuario = User.objects.get(email=usuario)
    queryset = Mapa.objects.filter(dueño=usuario)
    return render(request, 'carto/testingPato.html', {'mapas':queryset})

def mapaPato(request):
    return render(request, 'carto/testingPato.html')

@ensure_csrf_cookie
def loadMaps(request):
    usuario = request.POST.get('usuario')
    layers = serialize('geojson', Mapa.objects.get())
    return HttpResponse(layers, content_type='json')

def loadPoligonos(request, idMapa):
    poligonos = serialize('geojson', Poligono.objects.filter(mapa=idMapa))
    return HttpResponse(poligonos, content_type='json')

def loadPuntos(request, idMapa):
    puntos = serialize('geojson', Punto.objects.filter(mapa=idMapa))
    return HttpResponse(puntos, content_type='json')

def loadLineas(request, idMapa):
    lineas = serialize('geojson', CadenaLinea.objects.filter(mapa=idMapa))
    return HttpResponse(lineas, content_type='json')

def loadAll(request, idMapa):
    todos = list()
    poligonos = Poligono.objects.filter(mapa=idMapa)
    puntos = Punto.objects.filter(mapa=idMapa)
    lineas = CadenaLinea.objects.filter(mapa=idMapa)
    for x in puntos:
        todos.append(x)
    for x in poligonos:
        todos.append(x)
    for x in lineas:
        todos.append(x)
    test = serialize('geojson', todos)
    return HttpResponse(test, content_type='json')

def crearNuevoMapa(request):
    nombre = request.POST.get("nombre")
    usuario = User.objects.get(email=request.user)
    try:
        mapa = Mapa(nombre=nombre, dueño=usuario)
        mapa.save()
    except Mapa.DoesNotExist:
        mapa = null
    return HttpResponse(mapa.pk)

def eliminarMapa(request):
    idMapa = request.POST.get("idMapa")
    res = "null"
    try:
        mapa = Mapa.objects.get(pk=idMapa)
        mapa.delete();
        res = "Se elimino el mapa con exito"
    except Mapa.DoesNotExist:
        res = "No se pudo concretar la eliminación"
    return HttpResponse(res)

def actualizarNombreMapa(request):
    idMapa = request.POST.get("idMapa")
    nuevoNombre = request.POST.get("nuevoNombre")
    try:
        mapa = Mapa.objects.get(pk=idMapa)
        mapa.nombre = nuevoNombre
        mapa.save()
    except Mapa.DoesNotExist:
        mapa = null
    return HttpResponse(mapa)

def actualizar(request):
    temp = json.loads(request.POST.get('datos'))
    for layer in temp:
        type = layer['type']
        if(type == 'Point'):
            punto = Punto.objects.get(pk=layer['id'])
            punto.geometry = GEOSGeometry(json.dumps(layer['geom']))
            punto.save()
        if(type == 'Polygon'):
            poligono = Poligono.objects.get(pk=layer['id'])
            poligono.geometry = GEOSGeometry(json.dumps(layer['geom']))
            poligono.save()
        if(type == 'LineString'):
            cadenaLinea = CadenaLinea.objects.get(pk=layer['id'])
            cadenaLinea.geometry = GEOSGeometry(json.dumps(layer['geom']))
            print(json.dumps(layer['geom']))
            cadenaLinea.save()
    return HttpResponse("Modificación realizada")

def actualizarNombreGeometria(request):
    idGeometria = request.POST.get('idGeometria')
    type = request.POST.get('tipo')
    nuevoNombre = request.POST.get('nombre')
    if(type == 'Point'):
        punto = Punto.objects.get(pk=idGeometria)
        punto.nombre = nuevoNombre
        punto.save()
    if(type == 'Polygon'):
        poligono = Poligono.objects.get(pk=idGeometria)
        poligono.nombre = nuevoNombre
        poligono.save()
    if(type == 'LineString'):
        cadenaLinea = CadenaLinea.objects.get(pk=idGeometria)
        cadenaLinea.nombre = nuevoNombre
        cadenaLinea.save()
    return HttpResponse("Modificación realizada")

def insertar(request):
    nombre = request.POST.get('nombre')
    coords = request.POST.get('coordenadas')
    type = request.POST.get('tipo')
    idMapa = request.POST.get('idMapa')
    mapa = Mapa.objects.get(pk=idMapa)
    if(type == "Polygon"):
        poligono = Poligono(nombre=nombre, geometry=GEOSGeometry(coords), mapa=mapa)
        poligono.save()
    if(type == "Point"):
        punto = Punto(nombre=nombre, geometry=GEOSGeometry(coords), mapa=mapa)
        punto.save()
    if(type == 'LineString'):
        cadenaLinea = CadenaLinea(nombre=nombre, geometry=GEOSGeometry(coords), mapa=mapa)
        cadenaLinea.save()
    return HttpResponse("Se registro la figura con exito")

def eliminar(request):
    idLayer = request.POST.get('idLayer')
    type = request.POST.get('tipo')
    if(type == "Polygon"):
        Poligono.objects.filter(pk=idLayer).delete()
    if(type == "Point"):
        Punto.objects.filter(pk=idLayer).delete()
    if(type == 'LineString'):
        CadenaLinea.objects.filter(pk=idLayer).delete()
    return HttpResponse("Se elimino con exito")
