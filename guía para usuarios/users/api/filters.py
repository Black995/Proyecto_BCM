import django_filters
from django.contrib.auth import get_user_model
from erm_api.filters import EntityFilter

User = get_user_model()


class UserFilter(EntityFilter):
    is_an_area_manager = django_filters.BooleanFilter(
        field_name='area_manager', lookup_expr='isnull', exclude=True)
    is_an_area_erm_manager = django_filters.BooleanFilter(
        field_name='area_erm_manager', lookup_expr='isnull', exclude=True)

    class Meta:
        model = User
        fields = ('role',)
