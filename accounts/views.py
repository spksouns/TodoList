from email.policy import default
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import models

from datetime import datetime

#view classes which user could see

#task list view
class TaskList(LoginRequiredMixin, ListView):
    model = models.Task1
    context_object_name = 'tasklist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('searchdate') or ''
        context['tasklist'] = context['tasklist'].filter(
            user=self.request.user)
        now = datetime.now()
        context['now'] = now
        context['today'] = now.strftime("%Y-%m-%d")
        if search_input:
            context['tasklist'] = context['tasklist'].filter(
                created=search_input)
            context['searchdate'] = search_input
            context['count'] = context['tasklist'].filter(
                complete=False).count()
        else:
            context['tasklist'] = context['tasklist'].filter(
                created=context['today'])
            context['searchdate'] = context['today']
            context['count'] = context['tasklist'].filter(
                complete=False).count()
        return context

#used to create task
class TaskCreate(LoginRequiredMixin, CreateView):
    model = models.Task1
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

#used to update task
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = models.Task1
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')

#used to delete task
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = models.Task1
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')

#used for login
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy('task-list')

#used for new registration
class RegisterPage(FormView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task-list')
        return super(RegisterPage, self).get(*args, *kwargs)
