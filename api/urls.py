from django.urls import path
from . import views

urlpatterns = [
    path('testareas/<pk>', views.TestAreasView.as_view()),
    path('trackerfeed/<vehicle_no>', views.TrackerFeedView.as_view())
]