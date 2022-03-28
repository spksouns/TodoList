from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import models
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from . forms import UserRegisterForm
# view classes which user could see

# task list view


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

        def assigning(n):
            context['tasklist'] = context['tasklist'].filter(
                created=n)
            context['searchdate'] = n
            context['count'] = context['tasklist'].filter(
                complete=False).count()
        if search_input:
            assigning(search_input)
        else:
            assigning(context['today'])
        return context

# used to create task


class TaskCreate(LoginRequiredMixin, CreateView):
    model = models.Task1
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

# used to update task


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = models.Task1
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')

# used to delete task


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = models.Task1
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')

# used for login


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('adminpage')
        else:
            return reverse_lazy('task-list')

# used for new registration


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


class SignupView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('adminpage')


def crossoff(request, listid):
    model = models.Task1
    item = model.objects.get(pk=listid)
    item.completed = True
    return redirect('tasklist')


@user_passes_test(lambda u: u.is_superuser)
def adminpage(request):
    context_object_name = 'adminpage'
    return render(request, 'accounts/adminpage.html', {'user': request.user})


@user_passes_test(lambda u: u.is_superuser)
def members(request):
    display = models.User.objects.filter(is_superuser=False)
    return render(request, 'accounts/userdetails.html', {'displayname': display})


@user_passes_test(lambda u: u.is_superuser)
def MemberTask(request, pk):
    model = models.Task1
    context = {}
    search_input = request.GET.get('searchdate') or ''
    now = datetime.now()
    context['now'] = now
    context['today'] = now.strftime("%Y-%m-%d")
    context['display'] = model.objects.filter(user_id=pk)
    context['name'] = models.User.objects.filter(id=pk)

    def assigning(n):
        context['display'] = context['display'].filter(
            created=n)
        context['searchdate'] = n
        context['count'] = context['display'].filter(
            complete=False).count()
    if search_input:
        assigning(search_input)
    else:
        assigning(context['today'])
    return render(request, 'accounts/mytask.html', context)
