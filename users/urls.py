from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from users.views import UserUpdateView, UserView

urlpatterns = [
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('details/', UserView.as_view(), name='user-details'),
]