from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='pivot_table'),
    path('output', views.output, name='Output Test'),
    path('testmap', views.test_map, name='test_map'),
    path('polygonmap/<id>/', views.polygon_map, name='polygon_map'),
    path('kmloutput', views.kmloutput, name='kmloutput')
]