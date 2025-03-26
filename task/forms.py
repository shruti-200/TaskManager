from django import forms
from django.contrib.auth.models import User
from .models import Task


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")
        labels = {
            "username": "User Name",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Id",
        }

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        labels = {
            "username": "User Name",
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Id",
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "assigned_to", "status", "due_date")
        labels = {
            "name": "Task Name",
            "description": "Task Description",
            "assigned_to": "Assigned To",
            "status": "Status",
            "due_date": "Due Date",
        }
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }