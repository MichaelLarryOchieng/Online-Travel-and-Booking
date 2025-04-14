from django.contrib import admin
from django.urls import path
from . import views
#http://127.0.0.1:8000/location_app/api/locations/ (to view your API data)
#http://127.0.0.1:8000/location_app/locations_html/ (to view your HTML page)

urlpatterns = [
    path('api/locations/', views.LocationsList.as_view(), name='locations-list'),
    #url pattern, view, view name
    path('locations_html/', views.locations_html, name='locations-html'),
     #url pattern, view, view name
     path('', views.index, name='index')
]
