# hello
from django.urls import path
from . import views
urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('company/', views.getCompanyS, name='comp'),
    path('forms/', views.getForms, name='form'),
    path('metrics/', views.getMetrics, name='met'),
    path('performance/', views.getPerformance, name='perf'), ]
