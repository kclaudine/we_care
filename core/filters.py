from .models import *
import django_filters

class HouseFilter(django_filters.FilterSet):
    class Meta:
        model = House
        fields = ['district','sector','type','beds','baths']
