from django_tables2 import tables
from django_tables2.utils import A
from django_tables2.columns import LinkColumn

from tests.models import Test


class TestTable(tables.Table):
    title = LinkColumn("test-detail", args=[A("pk")])

    class Meta:
        model = Test
        row_attrs = {
            "href": lambda record: record.pk
        }