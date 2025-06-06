from django.urls import path
from . import views
from .views import assignment_list, assignment_submit, assignment_approve

urlpatterns = [
    path("", assignment_list, name="assignment_list"),
    path("submit/", assignment_submit, name="assignment_submit"),
    path("approve/<int:assignment_id>/", assignment_approve, name="assignment_approve"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/<int:task_id>/upload/", views.upload_assignment_for_task, name="upload_assignment_for_task"),
    path("review/", views.review_assignments, name="review_assignments"),
    path("review/<int:assignment_id>/", views.approve_assignment, name="approve_assignment"),
]