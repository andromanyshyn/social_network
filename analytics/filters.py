from django_filters import rest_framework as filters

from analytics.models import PostActivity


class PostAnalyticFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="occurred_at", lookup_expr="gte")
    date_to = filters.DateFilter(field_name="occurred_at", lookup_expr="lte")

    class Meta:
        model = PostActivity
        fields = ("date_from", "date_to")
