from django.contrib import admin

from tests.models import Test, TestCase

admin.site.register(Test)
admin.site.register(TestCase)
