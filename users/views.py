from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic import TemplateView, CreateView

from .forms import SignUpForm

from django.urls import reverse_lazy


class HomeView(TemplateView):
    template_name = 'auth/home.html'


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'auth/register.html'