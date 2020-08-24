from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView, CreateView

from .forms import SignUpForm, UserForm

from django.urls import reverse_lazy


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('test-list')
    template_name = 'auth/register.html'


class UserDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user-detail.html'


class UserUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    template_name = 'user/user-update.html'

    def post(self, request):

        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, file_data, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            # messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('user-details'))

        context = self.get_context_data(user_form=user_form,)

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
