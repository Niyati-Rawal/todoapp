from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import *

# Create your views here.
class customloginview(LoginView):
    template_name='todoapp/login.html'
    fields ='__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class registeruser(FormView):
    template_name = 'todoapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(registeruser, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(registeruser, self).get(*args, **kwargs)



class tasklist(LoginRequiredMixin,ListView):
    model = Task
    context_object_name='tasks'
# user will only able to see his/her todo list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context['count']=context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks']=context['tasks'].filter(title__startswith = search_input)
        
        context['search_input'] = search_input
        return context

class taskdetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name='task'
    template_name='todoapp/task.html'

class taskcreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    #form - validation
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super (taskcreate, self).form_valid(form)

class taskupdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

class taskdelete(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url = reverse_lazy('tasks')
