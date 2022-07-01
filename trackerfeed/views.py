from django.shortcuts import render
import pandas as pd
from trackerfeed.models import TestAreas, VtrackerTrackerfeed
from django.contrib.gis.db.models.functions import Centroid

# Create your views here.
def home(request):
    dict_movement = pd.read_csv('list_vehicle_moved.csv').to_dict('records')
    return render(request, 'home.html',{'data':dict_movement,'grid_type':"flat",'grid_total':"off",'grid_grandtotal':"off"})

def output(request):
    resp = TestAreas.objects.extra(where=["geometrytype(polygon) LIKE 'POLYGON'"]).order_by('branch_no','route_type','name')
    return render(request, 'output.html', {'areas':resp})

def test_map(request):
    resp = TestAreas.objects.all().extra(where=["geometrytype(polygon) LIKE 'POINT'"])
    return render(request, 'test_map.html',{'test':resp})

def polygon_map(request, id):
    area = TestAreas.objects.filter(id=id).annotate(cent=Centroid('polygon'))
    print(area)
    return render(request, 'polygonmap.html',{'area':area})

def vehicle_route(request):
    vehicles = VtrackerTrackerfeed.objects.filter(vehicle_no='BPN4762')
    return render(request, 'vehicle_route.html',{'vehicle'})

def kmloutput(request):
    return render(request, 'kmloutput.html')