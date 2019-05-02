from django.contrib.gis.db import models
from cuentas.models import User

class WorldBorder(models.Model):
    nombre = models.CharField(max_length=50)
    geom = models.MultiPolygonField(srid=4326)
    def __str__(self):
        return self.name

class Mapa(models.Model):
    nombre = models.CharField(max_length=50)
    dueño = models.ForeignKey(User,  on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Poligono(models.Model):
    nombre = models.CharField(max_length=50)
    geometry = models.PolygonField(srid=4326)
    mapa = models.ForeignKey(Mapa,  on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class Punto(models.Model):
    nombre = models.CharField(max_length=50)
    geometry = models.PointField(srid=4326)
    mapa = models.ForeignKey(Mapa,  on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class CadenaLinea(models.Model):
    nombre = models.CharField(max_length=50)
    geometry = models.LineStringField(srid=4326)
    mapa = models.ForeignKey(Mapa,  on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
