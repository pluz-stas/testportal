from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from users.views import UserUpdateView, UserDetailView

urlpatterns = [
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('details/', UserDetailView.as_view(), name='user-details'),
]