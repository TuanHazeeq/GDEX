from rest_framework import serializers
from trackerfeed.models import TestAreas, VtrackerTrackerfeed

class TestAreasSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestAreas
        fields = ['name','polygon','route_type','branch_no']

class TrackerFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = VtrackerTrackerfeed
        fields = ['vehicle_no', 'time_stamp', 'coordinate']