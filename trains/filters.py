import django_filters
from .models import Train


class TrainFilter(django_filters.FilterSet):
    departure_date = django_filters.DateFilter(field_name='departure_time', lookup_expr='date')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Train
        fields = ['source', 'destination', 'departure_date', 'min_price', 'max_price']