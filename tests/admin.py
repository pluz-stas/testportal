from django.contrib import admin

from tests.models import Test, TestCase, Answer, UserTests, Comment

admin.site.register(Test)
admin.site.register(UserTests)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(TestCase)
