from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import Comment
from assignments.models import Assignment, Task
from django.contrib import messages
from django.core.exceptions import PermissionDenied


@login_required
def add_comment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.assignment = assignment
            comment.user = request.user
            comment.save()
            return redirect("assignment_list")
    else:
        form = CommentForm()
    return render(request, "comments/add_comment.html", {"form": form, "assignment": assignment})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        raise PermissionDenied
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comentariul a fost modificat.")
            if comment.assignment:
                return redirect('assignment_detail', assignment_id=comment.assignment.id)
            else:
                return redirect('task_detail', task_id=comment.task.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comments/edit_comment.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        raise PermissionDenied
    if request.method == "POST":
        if comment.assignment:
            redirect_to = 'assignment_detail'
            redirect_id = comment.assignment.id
        else:
            redirect_to = 'task_detail'
            redirect_id = comment.task.id
        comment.delete()
        messages.success(request, "Comentariul a fost șters.")
        return redirect(redirect_to, redirect_id)
    return render(request, 'comments/confirm_delete.html', {'comment': comment})

@login_required
def add_comment_to_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.assignment = assignment
            comment.save()
            messages.success(request, "Comentariul a fost adăugat.")
            return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = CommentForm()
    return render(request, 'comments/add_comment.html', {'form': form})

@login_required
def add_comment_to_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.task = task
            comment.save()
            messages.success(request, "Comentariul a fost adăugat.")
            return redirect('task_detail', task_id=task.id)
    else:
        form = CommentForm()
    return render(request, 'comments/add_comment.html', {'form': form})

