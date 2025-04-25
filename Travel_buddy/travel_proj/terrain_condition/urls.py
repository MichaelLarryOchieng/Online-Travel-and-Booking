from django.urls import path
from . import views

urlpatterns = [
    path('terrain-condition/', views.get_terrain_condition_data, name='terrain_condition_data'),
    # ... other URL patterns
]