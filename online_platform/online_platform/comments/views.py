from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import Comment
from assignments.models import Assignment

@login_required
def add_comment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.assignment = assignment
            comment.author = request.user
            comment.save()
            return redirect("assignment_list")
    else:
        form = CommentForm()
    return render(request, "comments/add_comment.html", {"form": form, "assignment": assignment})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect("assignment_list")
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("assignment_list")
    else:
        form = CommentForm(instance=comment)
    return render(request, "comments/edit_comment.html", {"form": form, "comment": comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect("assignment_list")
