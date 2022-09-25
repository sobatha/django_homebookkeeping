
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class UserCreateView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super(UserCreateView, self).form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):

    def get_queryset(self):
        qs = super(UserUpdateView, self).get_queryset()
        return qs.filter(user=self.request.user)


