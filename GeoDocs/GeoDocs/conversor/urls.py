from django.conf.urls import url
from . import views
from .views import *
from django.contrib.auth.decorators import login_required

app_name='conversor'
urlpatterns = [
    url(r'^$', views.loadFormularioConversor, name="Conversor"),
    url(r'^exportar$', views.importarGeometria, name="exportar"),
    url(r'^update$', views.actualizar, name="update"),
    url(r'^calcular$', views.calcular, name="calcular"),

]
