from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableView

from tests.filters import TestFilter
from tests.forms import TestForm, TestCaseForm, AnswerForm, CommentForm
from tests.models import Test, TestCase, Answer, UserTests
from tests.tables import TestTable


class TestCompleteView(LoginRequiredMixin, TemplateView):
    template_name = "test/test-complete.html"

    def post(self, request, test_id: int = None):
        test = Test.objects.get(id=test_id)

        if request.POST and request.user:
            for answer in request.POST.getlist("answers"):
                try:
                    request.user.users_answers.add(int(answer))
                except ValueError:
                    break
                request.user.save()
            score = test.calculate_result(user=request.user)
            result = UserTests(user=request.user, test=test, score=score)
            result.save()
            return HttpResponseRedirect(redirect_to=reverse_lazy("test-detail", args=[str(test_id), ]))

        context = self.get_context_data(test=test)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer
    success_url = reverse_lazy("test-list")


class AnswerCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'test/answer-create.html'
    answer_form = AnswerForm

    def post(self, request, test_id=None, test_case_id=None):
        answer_form = AnswerForm(request.POST)

        if answer_form.is_valid():
            test_case = TestCase.objects.get(id=test_case_id)
            instance = answer_form.save(commit=False)
            if test_case_id:
                instance.test_case = test_case
            instance.save()
            return HttpResponseRedirect(reverse_lazy('test-update', args=[str(test_id), ]))

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
            return HttpResponseRedirect(reverse_lazy('test-update', args=[str(test_id), ]))

        context = self.get_context_data(test_case_form=test_case_form, )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request)


class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, test_id=None):
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            if test_id:
                instance.test = Test.objects.get(id=test_id)
                instance.user = request.user
            instance.save()
        return HttpResponseRedirect(reverse_lazy('test-detail', args=[str(test_id), ]))


class TestListView(LoginRequiredMixin, FilterView, SingleTableView):
    model = Test
    filterset_class = TestFilter
    table_class = TestTable
    template_name = "test/test-list.html"

    def get_queryset(self):
        queryset = super(TestListView, self).get_queryset()
        owned = self.request.GET.get('owned', None)
        completed = self.request.GET.get('completed', None)
        user = self.request.user or None
        if owned and user:
            queryset = queryset.filter(owner=user)
        if completed:
            queryset = queryset.filter(completed_by=self.request.user)
        return queryset


class TestDetailView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        comment_form = CommentForm()
        test = Test.objects.get(id=pk)
        request_user_results = UserTests.objects.filter(test=test).filter(test__completed_by=request.user)
        list_of_completes = UserTests.objects.filter(test=test)
        if list_of_completes:
            test.count = list_of_completes.count()
        if request_user_results:
            test.result = request_user_results.first().score
        test.score = test.testcase_set.all().aggregate(Sum("score")).get("score__sum", None)
        owner = request.user == test.owner
        return render(
            request, template_name="test/test-detail.html",
            context={
                "test": test,
                "owner": owner,
                "comment_form":comment_form,
                "warnings": test.get_warnings()
            }
                      )


class TestUpdateView(LoginRequiredMixin, TemplateView):
    test_form = TestForm
    template_name = "test/test-update.html"

    def post(self, request, test_id=None):
        test = Test.objects.get(id=test_id)
        if test.owner == request.user:
            test_form = TestForm(request.POST or None)
            if test_form.is_valid():
                test_form.save()
                return HttpResponseRedirect(reverse_lazy('test-details', args=[str(test.id),]))
            context = self.get_context_data(test_form=test_form, test=test, warnings=test.get_warnings())

            return self.render_to_response(context)
        else:
            return HttpResponse(status=403)

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
            return HttpResponseRedirect(reverse_lazy('test-detail', args=[str(instance.id), ]))

        context = self.get_context_data(test_form=test_form, )

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
