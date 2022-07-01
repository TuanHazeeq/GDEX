from rest_framework import generics
from .serializers import TestAreasSerializer, TrackerFeedSerializer
from trackerfeed.models import TestAreas, VtrackerTrackerfeed
from django.http import HttpResponse

# Create your views here.
class TestAreasView(generics.ListAPIView):
    serializer_class = TestAreasSerializer
    #queryset = TestAreas.objects.all()
    def get_queryset(self):
         id = self.kwargs['pk']
         return TestAreas.objects.filter(id=id)

class TrackerFeedView(generics.ListAPIView):
    serializer_class = TrackerFeedSerializer

    def get_queryset(self):
        return VtrackerTrackerfeed.objects.filter(vehicle_no=self.kwargs.get('vehicle_no'),
        time_stamp__range=["2022-04-15", "2022-04-30"])