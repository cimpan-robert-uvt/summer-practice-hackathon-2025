from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Assignment, Task
from .forms import AssignmentForm, TaskForm
from .utils import auto_review_assignment, auto_fix_suggestions
from django.contrib import messages
from comments.models import Comment
from django.contrib.admin.views.decorators import staff_member_required
from users.models import CustomUser
from django.shortcuts import render, get_object_or_404
from .models import Task


@login_required
def assignment_list(request):
    if request.user.is_teacher:
        assignments = Assignment.objects.all()
    else:
        assignments = Assignment.objects.filter(student=request.user)
    return render(request, "assignments/list.html", {"assignments": assignments})

@login_required
def assignment_submit(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.save()
            return redirect("assignment_list")
    else:
        form = AssignmentForm()
    return render(request, "assignments/submit.html", {"form": form})

@login_required
def assignment_approve(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.user.is_teacher:
        if request.method == "POST":
            assignment.approved = True
            assignment.grade = request.POST.get("grade")
            assignment.save()
            return redirect("assignment_list")
    return render(request, "assignments/approve.html", {"assignment": assignment})

@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    comments = assignment.comments.all().order_by("-created_at")
    return render(request, "assignments/assignment_detail.html", {
        "assignment": assignment,
        "comments": comments,
    })

def is_student(user):
    return hasattr(user, 'role') and user.role == 'student'

@login_required
@user_passes_test(is_student)
def upload_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.save()

            problems = auto_review_assignment(assignment)
            suggestions = auto_fix_suggestions(assignment)

            if problems:
                for issue in problems:
                    messages.warning(request, f"Auto-Review: {issue}")
            else:
                messages.success(request, "Auto-Review: Tema pare în regulă!")

            if suggestions:
                for fix in suggestions:
                    messages.info(request, f"Sugestie Auto-Fix: {fix}")

            return redirect("assignment_list")
    else:
        form = AssignmentForm()
    return render(request, "assignments/upload.html", {"form": form})

@login_required
@user_passes_test(lambda u: hasattr(u, 'role') and u.role == 'teacher')
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            messages.success(request, "Task created.")
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "assignments/create_task.html", {"form": form})

@login_required
def task_list(request):
    tasks = Task.objects.all().order_by("-deadline")
    return render(request, "assignments/task_list.html", {"tasks": tasks})

@login_required
@user_passes_test(is_student)
def upload_assignment_for_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.task = task
            assignment.save()
            messages.success(request, "Assignment sent.")
            return redirect("assignment_list")
    else:
        form = AssignmentForm()
    return render(request, "assignments/upload.html", {"form": form, "task": task})

@staff_member_required
def review_assignments(request):
    assignments = Assignment.objects.filter(status='pending').order_by('uploaded_at')
    return render(request, "assignments/review_assignments.html", {"assignments": assignments})

@staff_member_required
def approve_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        status = request.POST.get("status")
        comment = request.POST.get("approval_comment", "")
        if status in ['approved', 'rejected']:
            assignment.status = status
            assignment.approval_comment = comment
            assignment.save()
            messages.success(request, f"Assignment {status}.")
            return redirect("review_assignments")
    return render(request, "assignments/approve_assignment.html", {"assignment": assignment})

@login_required
def upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.save()
            messages.success(request, "Assignment sent.")
            return redirect("assignment_list")
    else:
        form = AssignmentForm()
    return render(request, "assignments/upload.html", {"form": form})

@login_required
def assignment_create(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.student = request.user
            assignment.task = task
            assignment.save()
            messages.success(request, "Assignment sent.")
            return redirect("assignment_list")
    else:
        form = AssignmentForm()
    return render(request, "assignments/upload.html", {"form": form, "task": task})

@login_required
@user_passes_test(lambda u: u.role == 'teacher')
def create_task_for_student(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id, role='student')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = student
            task.created_by = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'assignments/create_task_for_student.html', {'form': form, 'student': student})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'assignments/task_detail.html', {'task': task})

def dashboard_teacher(request):
    teacher_tasks = Task.objects.filter(created_by=request.user).select_related('assigned_to')
    return render(request, 'users/dashboard_teacher.html', {'teacher_tasks': teacher_tasks})