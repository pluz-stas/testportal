from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from tests.filters import TestFilter
from tests.forms import TestForm, TestCaseForm, AnswerForm
from tests.models import Test, TestCase, Answer


# class TestCompleteView(LoginRequiredMixin, TemplateView):


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer
    success_url = reverse_lazy("test-list")


class AnswerCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'test/answer-create.html'
    answer_form = AnswerForm

    def post(self, request, test_id=None, test_case_id=None):
        answer_form = AnswerForm(request.POST)

        if answer_form.is_valid():
            instance = answer_form.save(commit=False)
            if test_case_id:
                instance.test_case = TestCase.objects.get(id=test_case_id)
            instance.save()
            return HttpResponseRedirect(reverse_lazy('test-update', args=[str(test_id),]))

        context = self.get_context_data(answer_form=answer_form, )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request)


class TestCaseCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'test/test_case-create.html'
    test_case_form = TestCaseForm

    def post(self, request, test_id=None):
        test_case_form = TestCaseForm(request.POST)

        if test_case_form.is_valid():
            instance = test_case_form.save(commit=False)
            if test_id:
                instance.test = Test.objects.get(id=test_id)
            instance.save()
            return HttpResponseRedirect(reverse_lazy('test-update', args=[str(test_id),]))

        context = self.get_context_data(test_case_form=test_case_form, )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request)


class TestListView(LoginRequiredMixin, FilterView):
    model = Test
    filterset_class = TestFilter
    template_name = "test/test-list.html"

    def get_queryset(self):
        queryset = super(TestListView, self).get_queryset()
        owned = self.request.GET.get('owned', None)
        user = self.request.user or None
        if owned and user:
            queryset = queryset.filter(owner=user)
        return queryset


class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = "test/test-detail.html"


class TestUpdateView(LoginRequiredMixin, TemplateView):
    test_form = TestForm
    template_name = "test/test-update.html"

    def post(self, request, test_id=None):
        test = Test.objects.get(id=test_id)
        test_form = TestForm(request.POST or None)

        if test_form.is_valid():
            test_form.save()
            # messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('user-details'))
        context = self.get_context_data(test_form=test_form, test=test)

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):

        return self.post(request, *args, **kwargs)


class TestCreateView(LoginRequiredMixin, TemplateView):
    test_form = TestForm
    template_name = 'test/test-create.html'

    def post(self, request):

        test_form = TestForm(request.POST)

        if test_form.is_valid():
            instance = test_form.save(commit=False)
            instance.owner = request.user
            instance.save()
            # messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('test-detail', args=[str(instance.id),]))

        context = self.get_context_data(test_form=test_form,)

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
