from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_safe
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.conf.urls import handler500
from django.db import transaction
from .forms import SignUpForm, UserEditForm, TaskForm
from django.contrib.auth.models import User
from .models import Task

# Create your views here.
@require_safe
def home(request):
    return render(request, 'home.html')
    
@require_safe
def aboutus(request):
    return render(request, 'aboutus.html')

@require_http_methods(["GET","POST"])
def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

@require_http_methods(["GET","POST"])
@transaction.atomic
def register_user(request):
    try:
        if request.method == 'GET':
            user_form = SignUpForm()
            return render(request, 'signup.html', {"u_form": user_form})
        if request.method == 'POST':
            user_form = SignUpForm(request.POST)

            if user_form.is_valid():
                user = user_form.save()
                user.save()
                return redirect('login')
            else:
                user_form = SignUpForm(request.POST)

                for field in user_form.errors:
                    user_form[field].field.widget.attrs['class'] += ' error'
                return render(request, 'signup.html', {"u_form": user_form})
    except Exception:
        return redirect(handler500)
    


@require_safe
def task(request):
    if request.user.is_superuser:
        tasks = Task.objects.filter(status__in=["To-Do", "In-Progress"])  
    else:
        tasks = Task.objects.filter(assigned_to=request.user, status__in=["To-Do", "In-Progress"])

    return render(request, 'task.html', {"tasks": tasks})

def task_form_add_update(request, id=0):
    try:
        if request.method == 'GET':
            if id == 0:
                m_form = TaskForm()
            else:
                task = Task.objects.get(id=id)
                m_form = TaskForm(instance=task)
            return render(request, 'task_form.html', {'m_form': m_form})
        if request.method == 'POST':
            if id==0:
                m_form = TaskForm(request.POST, request.FILES)
            else:
                task = Task.objects.get(id=id)
                m_form = TaskForm(request.POST, instance=task)
            if m_form.is_valid():
                new_status = request.POST.get("status")
                task = Task.objects.get(id=m_form.instance.id)
                task_status = task.status
                if new_status == "Completed" and task_status != "Review":
                    messages.error(request, "You can only mark a task as 'Completed' after it has been reviewed.")
                    return redirect("task")
                m_form.save()
            else:
                for field in m_form.errors:
                    m_form[field].field.widget.attrs['class'] += ' error'
                return render(request, 'task_form.html', {'m_form': m_form})
            return redirect('task')
        return render(request, 'task.html')
    except Exception:
        return redirect(handler500)

@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    
    if request.user.is_superuser or task.assigned_to == request.user:
        task.delete()
        messages.success(request, "Task deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this task.")

    return redirect('task')


@login_required
def review(request):
    if request.user.is_superuser:
        tasks = Task.objects.filter(status="Review")  
    else:
        tasks = Task.objects.filter(assigned_to=request.user, status="Review") 

    return render(request, 'review.html', {"tasks": tasks})

@login_required
def history(request):
    if request.user.is_superuser:
        tasks = Task.objects.filter(status__in=["Completed", "Cancelled"]) 
    else:
        tasks = Task.objects.filter(assigned_to=request.user, status__in=["Completed", "Cancelled"])

    return render(request, 'history.html', {"tasks": tasks})
