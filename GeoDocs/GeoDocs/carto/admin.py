from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from leaflet.forms.widgets import LeafletWidget
from .models import WorldBorder,Mapa,Poligono,Punto,CadenaLinea

admin.site.register(WorldBorder, LeafletGeoAdmin)
admin.site.register(Mapa)
admin.site.register(Poligono, LeafletGeoAdmin)
admin.site.register(Punto, LeafletGeoAdmin)
admin.site.register(CadenaLinea, LeafletGeoAdmin)
