from django.contrib import admin

from tests.models import Test, TestCase, Answer

admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(TestCase)
