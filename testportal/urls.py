from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from users.views import HomeView, SignUpView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('register/', SignUpView.as_view(), name="register"),
]
