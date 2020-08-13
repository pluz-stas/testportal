from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django_filters.views import FilterView

from tests.models import Test
from tests.views import TestCreateView, TestDetailView, TestListView
from users.views import UserUpdateView, UserView

urlpatterns = [
    path('create/', TestCreateView.as_view(), name='test-create'),
    path('list/', TestListView.as_view(), name='test-list'),
    path('detail/<int:pk>/', TestDetailView.as_view(), name='test-detail'),
]