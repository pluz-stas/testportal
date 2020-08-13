import django_filters
from tests.models import Test

class TestFilter(django_filters.FilterSet):

    class Meta:
        model = Test
        fields = {
            "title": ["icontains"],
            "description": ["icontains"]
        }