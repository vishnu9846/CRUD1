from django.shortcuts import render,get_object_or_404,redirect
from .models import Task,Registration
from django.contrib import messages
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login  
from django.contrib.auth import logout
from django.urls import reverse

from rest_framework import viewsets
from .serializers import TaskSerializer


def table (request):
    tasks = Task.objects.all()
    
    return render(request,'table/table.html', {'tasks': tasks})


def task(request):
    tasks = Task.objects.all()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            description = form.cleaned_data['description']
            priority = form.cleaned_data['priority']
            assignee = form.cleaned_data['assignee']
            completion_status = form.cleaned_data['completion_status']
            
            task = Task(
                task_name=task_name,
                description=description,
                priority=priority,
                assignee=assignee,
                completion_status=completion_status
            )
            task.save()
            
            return redirect('crud:task')
    else:
        form = TaskForm()

    return render(request, 'table/task.html', {'form': form, 'tasks': tasks})

def update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('crud:table')
    else:
        form = TaskForm(instance=task)
    return render(request, 'table/task.html', {'form': form})


def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completion_status = not task.completion_status
    task.save()
    return redirect('crud:table')



def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('crud:table')


def account(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        form = LoginForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            messages.success(request, "Registration successful!")
            return redirect('crud:account')
        elif form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('crud:table')
                else:
                    messages.error(request, "Inactive account.")
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Invalid form submissions.")

    else:
        user_form = UserCreationForm()
        form = LoginForm()

    return render(request, 'register/account.html', {'user_form': user_form, 'form': form})


def signout(request):
    logout(request)
    return redirect(reverse('crud:account')) 

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    