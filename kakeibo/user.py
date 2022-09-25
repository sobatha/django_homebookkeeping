from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class UserCreateView(LoginRequiredMixin, CreateView):
    success_message = ''

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return super(UserCreateView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class UserUpdateView(LoginRequiredMixin, UpdateView):

    def get_queryset(self):
        qs = super(UserUpdateView, self).get_queryset()
        return qs.filter(user=self.request.user)


