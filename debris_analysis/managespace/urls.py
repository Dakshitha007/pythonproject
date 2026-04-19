from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('analysis/', views.analysis, name='analysis'),
    path('about/', views.about, name='about'),
    path('mongodb/', views.mongodb_demo, name='mongodb'),
]