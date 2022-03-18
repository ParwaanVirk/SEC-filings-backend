# hello
from django.urls import path
from company import views

from company.views import CompanyData, CompareComp, Favourites
urlpatterns = [
    path('company/', CompanyData.as_view(), name='comp'),
    path('favourites/', Favourites.as_view(), name='favourites'),
    path('compare_comp/', CompareComp.as_view(), name='compare_comp'),
    # path('forms/', views.getForms, name='form'),
    # path('metrics/', views.getMetrics, name='met'),
    # path('performance/', views.getPerformance, name='perf'),
    ]
