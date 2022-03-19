# hello
from django.urls import path
from company import views

from company.views import CompanyData, CompareComp, Favourites, CompSearch, Mostsearch, Seeding
urlpatterns = [
    path('company/', CompanyData.as_view(), name='comp'),
    path('favourites/', Favourites.as_view(), name='favourites'),
    path('compare_comp/', CompareComp.as_view(), name='compare_comp'),
    path('search/', CompSearch.as_view(), name = 'search'),
    path('most_searched/', Mostsearch.as_view(), name = 'most_search'),
    path('seeder/', Seeding.as_view(), name = 'seeder')
    ]
