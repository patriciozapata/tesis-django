from django.shortcuts import render
from conversor.forms import FormularioConversor
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.gis.geos import GEOSGeometry
import math
import json, math
from carto.models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from cuentas.models import User


User = get_user_model()

@csrf_exempt
def loadFormularioConversor(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(email=request.user)
        queryset = Mapa.objects.filter(dueño=usuario)
        return render(request, 'conversor/conversor.html', {'mapas':queryset})
    else:
        return render(request, 'conversor/conversor.html')

@csrf_exempt
#METODO PARA ACTUALIZAR PARAMETROS DE CALCULO
def actualizar(request):
    if request.is_ajax():
        proyeccion = request.POST.get('proyeccion')
        hemisferio = request.POST.get('hemisferio')
        htpl = request.POST.get('htpl')
        fnorte = 0
        feste = 0
        escala = 0
        if proyeccion == 'UTM':
            escala = 0.9996
            feste = 500000
            if(hemisferio == 'Norte'):
                fnorte = 0
            else:
                fnorte = 10000000
        elif proyeccion == 'PTL':
            escala = (int(htpl) + 6378000) / 6378000
            feste = 200000
            if hemisferio == 'Norte':
                fnorte = 0
            else:
                fnorte = 7000000
        elif proyeccion == 'LTM':
            escala = 0.999995
            feste = 200000
            if(hemisferio == 'Norte'):
                fnorte = 0
            else:
                fnorte = 7000000
        data = {'fnorte':fnorte, 'feste':feste, 'escala':escala}
    return HttpResponse(json.dumps(data))
@csrf_exempt
def calcular(request):
    if request.is_ajax():
        parametros = json.loads(request.POST.get('parametros'))
        coordGEOTM = json.loads(request.POST.get('geotm'))
        coordTMGEO = json.loads(request.POST.get('tmgeo'))
        achatamiento =float(parametros['achatamiento'])
        a = float(parametros['parametroA'])
        b = float(parametros['parametroB'])
        ex1 = float(parametros['excentricidad1'])
        ex2 = float(parametros['excentricidad2'])
        #Obtener datos de la proyección
        fn =float(parametros['falsoNorte'])
        fe =float(parametros['falsoEste'])
        k0 =float(parametros['factEscala'])
        mc =float(parametros['meridianoCentral'])
        pi = 3.14159265358979
        dios = []
        geotm = []
        tmgeo = []
        geotm = calcularGEOTM(achatamiento, a, b, ex1, ex2, fn, fe, k0, mc, coordGEOTM, pi)
        tmgeo = calcularTMGEO(achatamiento, a, b, ex1, ex2, fn, fe, k0, mc, coordTMGEO, pi)
        dios.append(geotm)
        dios.append(tmgeo)
        return HttpResponse(json.dumps(dios))
def calcularGEOTM(achatamiento, a, b, ex1, ex2, fn, fe, k0, mc, coordGEOTM, pi):
        listado = []
        seriGT = []
        for co in coordGEOTM:
            print("Wololooooooooooooooooooo")
            print(co['latitud']);
            lat_pto1 = float(co['latitud'])
            lon_pto1 = float(co['longitud'])
            #Secuencia de calculo para cada coordenada en el foreach
            s = math.sin((lat_pto1*pi)/180)
            c = math.cos((lat_pto1*pi)/180)
            t = math.tan((lat_pto1*pi)/180)
            #Calculo arco
            arco = arcoMeridiano(lat_pto1, a, b, k0)
            p = ((lon_pto1 - mc) * (pi/180))
            vv = a / ((1-(ex1**2)*(s**2))**(1/2))*k0
            ro = (a*(1-ex1**2))/((1-ex1**2*s**2)**(3/2))*k0
            nu = (vv / ro)-1
            I = arco + fn
            II = vv * s * c / 2
            III = vv * s * (c**3) * (5-(t**2)+9*nu) / 24
            IIIA = vv * s * c**5 * (61-58*t**2+t**4) / 720
            IV = vv * c
            V = (vv * (c ** 3) * ((vv / ro) - (t ** 2))) / 6
            VI = vv * (c ** 5) * (5 - 18 * (t ** 2) + (t ** 4) + 14 * nu - 58 * (t ** 2) * nu) / 120
            # Latitud y longitud
            nor_pto1 = I + p**2 * II + p**4 * III + p**6 * IIIA
            est_pto1 = fe + p * IV + (p ** 3) * V + (p ** 5) * VI
            #print("est1:" +str(nor_pto1))
            temp = {'norte':nor_pto1, 'este':est_pto1, 'arco':arco}
            serialize = {nor_pto1,est_pto1}
            seriGT.append(serialize)
            listado.append(temp)
            print(seriGT)
        return listado
        return seriGT
def calcularTMGEO(achatamiento, a, b, ex1, ex2, fn, fe, k0, mc, coordTMGEO, pi):
    listado = []
    serial = []
    for co in coordTMGEO:
        nor_pto = float(co['norte'])
        est_pto = float(co['este'])
        #calculos
        lat_aprox = (nor_pto - fn) / (a * k0)
    #print("est:" +str(lat_aprox))
        lat_aprox = lat_aprox * 180 / pi
        arco = arcoMeridiano(lat_aprox, a, b, k0)
        lat_pto = (nor_pto - fn - arco) / (a * k0)
        lat_pto = lat_pto * 180 / pi
        lat_pto = lat_pto + lat_aprox
        #segunda iteracion
        lat_aprox = lat_pto
        arco = arcoMeridiano(lat_aprox, a, b, k0)
        lat_pto = (nor_pto - fn - arco) / (a * k0)
        lat_pto = lat_pto * 180 / pi
        lat_pto = lat_pto + lat_aprox
        #tercera iteracion
        lat_aprox = lat_pto
        arco = arcoMeridiano(lat_aprox, a, b, k0)
        lat_pto = (nor_pto - fn - arco) / (a * k0)
        lat_pto = lat_pto * 180 / pi
        lat_pto = lat_pto + lat_aprox
        #cuarta iteracion
        lat_aprox = lat_pto
        arco = arcoMeridiano(lat_aprox, a, b, k0)
        lat_pto = (nor_pto - fn - arco) / (a * k0)
        lat_pto = lat_pto * 180 / pi
        lat_pto = lat_pto + lat_aprox
        #quinta iteracion
        lat_aprox = lat_pto
        arco = arcoMeridiano(lat_aprox, a, b, k0)
        lat_pto = (nor_pto - fn - arco) / (a * k0)
        lat_pto = lat_pto * 180 / pi
        lat_pto = lat_pto + lat_aprox #latitud definitiva

        #secuencia de calculos
        s = math.sin((lat_pto * pi)/180)
        c = math.cos((lat_pto * pi)/180)
        t = math.tan((lat_pto * pi)/180)
        sec = 1 / c
        #radianes de corvatura
        vv = a / ((1 - ex1**2 * s**2)**(1/2))*k0
        ro = (a * (1 - ex1 **2)) / ((1- ex1**2 * s**2)**(3/2)) * k0
        nu = vv / ro - 1
        #factores
        VII = t / (2 * ro * vv)
        VIII = (t / (24 * ro * vv ** 3)) * (5 + 3 * t ** 2 + nu - 9 * t ** 2 * nu ** 2)
        IX = (t / (720 * ro * vv ** 5)) * (61 + 90 * t ** 2 + 45 * t ** 4)
        Et = est_pto - fe
        X = sec / vv
        XI = (sec / (6 * vv**3)) * (vv / ro + 2 * t**2)
        XII = (sec / (120 * vv**5)) * (5 + 28 * t**2 + 24 * t**4)
        XIII = (sec / (5040 * vv**7)) * (61 + 662 * t**2 + 1320 * t**4 + 720 * t**6)
        #calcular Latitud y loongitud
        lat_pto = lat_pto * pi / 180 -Et**2 * VII + Et**4 * VIII - Et**6 * IX
        lat_pto = lat_pto * 180 / pi
        lon_pto =  mc * pi / 180 + Et * X - Et**3 * XI + Et**5 * XII - Et**7 * XIII
        lon_pto = lon_pto * 180 / pi
        #print("LAT:" +str(lat_pto))
    #    print("LON:" +str(lon_pto))
        temp = {'latitud': lat_pto,'longitud':lon_pto,'arco':arco}
        templitsa = {lat_pto, lon_pto}
        listado.append(temp)
        serial.append(templitsa)
    return listado
    return serial

def importarGeometria(request):
    mapa = Mapa.objects.get(pk=request.POST.get('idMapa'))
    nombre = request.POST.get('nombre')
    listado = json.loads(request.POST.get('lstGEOTM'))
    tipo = request.POST.get('tipo')
    test = {"type": "Polygon","coordinates": "coords"}
    coordinates = []
    if tipo == "ll":
        for puntos in listado:
            temp = []
            temp.append(float(puntos['latitud']))
            temp.append(float(puntos['longitud']))
            coordinates.append(temp)
    else:
        for puntos in listado:
            temp = []
            temp.append(float(puntos['norte']))
            temp.append(float(puntos['este']))
            coordinates.append(temp)
    test['coordinates'] = coordinates

    if(len(coordinates)>=4):
        if coordinates[-1] == coordinates[0]:
            test['type']="Polygon"
            test['coordinates']=[coordinates]
        else:
            test['type']="LineString"
    else:
        if(len(coordinates)==1):
            print("Es puntito")
            test['coordinates']=coordinates[0]
            test['type']="Point"
        else:
            test['type']="LineString"
    geometry = json.dumps(test)
    print(test)
    try:
        if(test['type'] == "Polygon"):
            poligono = Poligono(nombre=nombre, geometry=GEOSGeometry(geometry), mapa=mapa)
            poligono.save()
        if(test['type'] == "Point"):
            punto = Punto(nombre=nombre, geometry=GEOSGeometry(geometry), mapa=mapa)
            punto.save()
        if(test['type'] == 'LineString'):
            cadenaLinea = CadenaLinea(nombre=nombre, geometry=GEOSGeometry(geometry), mapa=mapa)
            cadenaLinea.save()
    except:
        return HttpResponse("Geometria no valida para ser registrada")
    return HttpResponse("Se guardo con exito")

def sexaRad(angulo):
    pi = 3.14159265358979
    sexarad = (angulo*pi)/180
    return sexarad
def arcoMeridiano(lat, radioA, radioB, factEscala):
    radioA = float(radioA)
    radioB = float(radioB)
    #Transformación latitud en radianes
    ladRad = sexaRad(lat)
    #Calcular el valor de n
    n = (radioA - radioB)/(radioA + radioB)
    #Calculo de los factores
    fac1 = (1 + n) + ((5/4)*(n**2)) + ((5/4)*(n**3))
    fac2 = (3 * n) + 3 * (n ** 2) + (21 / 8) * (n ** 3)
    fac3 = (15 / 8) * (n ** 2) + (15 / 8) * (n ** 3)
    fac4 = ((35 / 24) * (n ** 3))
    fact1 = fac1 * ladRad
    fact2 = fac2 * math.sin(ladRad) * math.cos(ladRad)
    fact3 = fac3 * math.sin(2*ladRad) * math.cos(2*ladRad)
    fact4 = fac4 * math.sin(3*ladRad) * math.cos(3*ladRad)
    arco = fact1-fact2+fact3-fact4
    arcoMeridiano = radioB * factEscala * arco
    return arcoMeridiano
