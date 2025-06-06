from django.urls import path
from . import views

urlpatterns = [
    path("", views.assignment_list, name="assignment_list"),
    path("<int:pk>/", views.assignment_detail, name="assignment_detail"),
    path("create/<int:task_id>/", views.assignment_create, name="assignment_create"),
    path("submit/", views.assignment_submit, name="assignment_submit"),
    path("approve/<int:assignment_id>/", views.assignment_approve, name="assignment_approve"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/<int:task_id>/upload/", views.upload_assignment_for_task, name="upload_assignment_for_task"),
    path("review/", views.review_assignments, name="review_assignments"),
    path("review/<int:assignment_id>/", views.approve_assignment, name="approve_assignment"),
    path('create_for_student/<int:student_id>/', views.create_task_for_student, name='create_task_for_student'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
]