from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_safe
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.conf.urls import handler500
from django.db import transaction
from .forms import SignUpForm, UserEditForm
from django.contrib.auth.models import User

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
    

@login_required
def user_details(request):
    try:
        if request.user.is_authenticated:
            if request.method == "POST":
                user_form = UserEditForm(request.POST, instance=request.user)
                if user_form.is_valid():
                    user_form.save()
                    return redirect('user_details')
                else:
                    for field in user_form.errors:
                        user_form[field].field.widget.attrs['class'] += ' error'
                    return render(request, 'user_details.html', {"u_form": user_form})
            else:
                user_form = UserEditForm(instance=request.user)
            return render(request, 'user_details.html', {"u_form": user_form})
    except Exception:
        return redirect(handler500)