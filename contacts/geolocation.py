from django import forms
from django.db import models
from django.utils.safestring import mark_safe

DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 400

DEFAULT_LAT = 39.63
DEFAULT_LNG = 2.94


class LocationWidget(forms.TextInput):
    def __init__(self, *args, **kw):

        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)

        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        if value is None:
            lat, lng = DEFAULT_LAT, DEFAULT_LNG
            zoom = 10
        else:
            zoom = 13
            if isinstance(value, unicode):
                a, b = value.split(',')
            else:
                a, b = value
            lat, lng = float(a), float(b)

        js = '''
<script type="text/javascript">
//<![CDATA[
    var map_%(name)s;
    var marker_%(name)s;
    
    function savePosition_%(name)s(point)
    {
        var input = document.getElementById("id_%(name)s");
        input.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
        map_%(name)s.panTo(point);
    }
    
    function load_%(name)s() {
        var point = new google.maps.LatLng(%(lat)f, %(lng)f);

        var options = {
            zoom: %(zoom)s,
            center: point,
            mapTypeId: google.maps.MapTypeId.ROADMAP
            // mapTypeControl: true,
            // navigationControl: true
        };
        
        map_%(name)s = new google.maps.Map(document.getElementById("map_%(name)s"), options);

        marker_%(name)s = new google.maps.Marker({
                map: map_%(name)s,
                position: new google.maps.LatLng(%(lat)f, %(lng)f),
                draggable: true
        
        });
        google.maps.event.addListener(marker_%(name)s, 'dragend', function(mouseEvent) {
            savePosition_%(name)s(mouseEvent.latLng);
        });

        google.maps.event.addListener(map_%(name)s, 'click', function(mouseEvent){
            marker_%(name)s.setPosition(mouseEvent.latLng);
            savePosition_%(name)s(mouseEvent.latLng);
        });

    }
    

//]]>
</script>
        ''' % dict(name=name, lat=lat, lng=lng,zoom=zoom)
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat, lng), dict(id='id_%s' % name))
        html += '<div id="map_%s" style="width: %dpx; height: %dpx"></div>' % (name, self.map_width, self.map_height)

        return mark_safe(js + html)

    class Media:
        js = (
            'http://maps.google.com/maps/api/js?sensor=false',
        )

class LocationFormField(forms.CharField):
    def clean(self, value):
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value

        lat, lng = float(a), float(b)
        if lat == DEFAULT_LAT and lng == DEFAULT_LNG:
            return None;        
            
        return "%f,%f" % (lat, lng)

class LocationField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': LocationFormField}
        defaults.update(kwargs)
        defaults['widget'] = LocationWidget
        return super(LocationField, self).formfield(**defaults)
