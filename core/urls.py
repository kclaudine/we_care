from django.urls import path, include
from .views import *

urlpatterns = [
   path('', home, name = 'home'),
   path('signup/', signup, name='signup'),
   path('about.html/', about, name='about'),
   path('search/', search_house, name='search'),
   path('sell_house/', new_house, name='sell'),
   path('houses_for_renting/', house_rent, name='house_rent'),
   path('houses_for_selling/', house_sell, name='house_sell'),
   path('profile/<str:username>/', profile, name='profile'),
   path('house_details/<pk>/', house_details, name='house_details')
]