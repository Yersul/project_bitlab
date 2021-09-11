from django.db.models import Q
from django_filters import rest_framework as filters
from products.models import Product


class ProductFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('name', 'description', 'owner', 'min_price', 'max_price')

    def filter_by_name(self, queryset, name, value):
        query = Q()
        query &= Q(name__contains=value)
        result = queryset.filter(query)
        return result

    def filter_by_description(self, queryset, name, value):
        filter_params = Q()
        filter_params |= Q(description__contains = value)
        result = queryset.filter(filter_params)
        return result
