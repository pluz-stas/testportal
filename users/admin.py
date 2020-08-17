from django.contrib import admin

from tests.models import UserTests
from users.models import User


class UsersTestsInline(admin.TabularInline):
    model = UserTests
    extra = 1


@admin.register(User)
class User(admin.ModelAdmin):
    inlines = (UsersTestsInline,)
    exclude = ("password",)