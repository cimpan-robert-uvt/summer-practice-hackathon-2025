from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from online_platform.online_platform.assignments.models import Task


# Create your views here.
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = task.comments.all().order_by("-created_at")
    return render(request, "assignments/task_detail.html", {
        "task": task,
        "comments": comments,
    })
