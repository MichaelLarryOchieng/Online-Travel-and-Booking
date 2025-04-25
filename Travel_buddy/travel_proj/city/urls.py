from django .urls import path, include
from city import views

urlpatterns = [
    path('cities/', views.CityListView.as_view()),
]