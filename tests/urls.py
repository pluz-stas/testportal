from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django_filters.views import FilterView

from tests.models import Test
from tests.views import TestCreateView, TestDetailView, TestListView, TestUpdateView, TestCaseCreateView
from users.views import UserUpdateView, UserView

urlpatterns = [
    path('create/', TestCreateView.as_view(), name='test-create'),
    path('update/<int:test_id>/test_case/create/', TestCaseCreateView.as_view(), name='test_case-create'),
    path('update/<int:test_id>/', TestUpdateView.as_view(), name='test-update'),
    path('list/', TestListView.as_view(), name='test-list'),
    path('detail/<int:pk>/', TestDetailView.as_view(), name='test-detail'),
]