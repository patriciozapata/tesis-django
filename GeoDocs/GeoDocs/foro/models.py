from django.db import models
from cuentas.models import User
from django.contrib import admin
from datetime import datetime
from django.utils.html import mark_safe
from markdown import markdown
from django.db.models.signals import post_save
from notifications.signals import notify
#from topicos.models import Topicos


class Topico(models.Model):
    nombre = models.CharField(max_length=100,unique=True,blank=False)
    def __str__(self):
        return (self.nombre)

class Categoria(models.Model):
    nombre = models.CharField( max_length=50,unique=True,blank=False)
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE)
    def __str__(self):
        return (self.nombre)

class Post(models.Model):
    titulo = models.CharField(max_length=50,unique=True,blank=False)
    descripcion = models.CharField(max_length=1000,blank=False)
    fecha = models.DateField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    def __str__(self):
        return (self.titulo)

class Visitas(models.Model):
    visita = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)


class Comentario(models.Model):
    comentario = models.CharField("Comentario", max_length=1000,blank=False)
    fecha = models.DateField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    def __str__(self):
        return (self.comentario)
    def get_message_as_markdown(self):
            return mark_safe(markdown(self.comentario, safe_mode='escape'))


class Like(models.Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
