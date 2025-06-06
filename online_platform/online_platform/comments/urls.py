from django.urls import path
from .views import add_comment, edit_comment, delete_comment
from . import views

urlpatterns = [
    path("add/<int:assignment_id>/", add_comment, name="add_comment"),
    path("edit/<int:comment_id>/", edit_comment, name="edit_comment"),
    path("delete/<int:comment_id>/", delete_comment, name="delete_comment"),
    path('assignment/<int:assignment_id>/comment/', views.add_comment_to_assignment, name='add_comment_to_assignment'),
    path('task/<int:task_id>/comment/', views.add_comment_to_task, name='add_comment_to_task'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]