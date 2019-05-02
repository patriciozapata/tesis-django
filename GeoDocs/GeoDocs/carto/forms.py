from django.contrib.gis import forms
from django.views.generic import UpdateView
from leaflet.forms.widgets import LeafletWidget

from .models import WorldBorder


class WorldBorderForm(forms.Form):
    class Meta:
        name = WorldBorder
        fields = ('name', 'geom')
        widgets = {'geom': LeafletWidget()}

class EditWorldBorder(UpdateView):
    model = WorldBorder
    form_class = WorldBorderForm
    template_name = 'carto/mapa.html'

class MyGeoForm(forms.Form):
    point = forms.MultiPolygonField(widget=forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))
