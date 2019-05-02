from django.db import models


# Create your models here.
class Tipo(models.Model):
    nombre = models.CharField(max_length=50,unique=True,blank=False)
    def __str__(self):
        return (self.nombre)

class Documentos(models.Model):
    nombre = models.CharField(max_length=500,unique=True,blank=False)
    autor = models.CharField(max_length=500,blank=False)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    fecha = models.DateField()
    resumen = models.CharField(max_length=2000,blank=False)
    docfile = models.FileField(upload_to="documents/%Y/%m/%d")

    def __str__(self):
        return (self.nombre)
