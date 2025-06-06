from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from assignments.models import Task


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    if request.user.role == 'teacher':
        teacher_tasks = Task.objects.filter(created_by=request.user)
        return render(request, "users/dashboard_teacher.html", {"teacher_tasks": teacher_tasks})
    else:
        return render(request, "users/dashboard_student.html")


@login_required
@user_passes_test(lambda u: u.role == 'teacher')
def search_students(request):
    query = request.GET.get('q', '')
    students = []
    if query:
        students = CustomUser.objects.filter(role='student', username__icontains=query)
    return render(request, 'users/search_students.html', {'students': students, 'query': query})