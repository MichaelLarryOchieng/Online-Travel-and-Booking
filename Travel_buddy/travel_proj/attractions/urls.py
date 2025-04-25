from django.urls import path
from attractions import views

urlpatterns = [
    path('attractions/', views.AttractionListView.as_view()),
    ]