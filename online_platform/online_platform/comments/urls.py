from django.urls import path
from .views import add_comment, edit_comment, delete_comment

urlpatterns = [
    path("add/<int:assignment_id>/", add_comment, name="add_comment"),
    path("edit/<int:comment_id>/", edit_comment, name="edit_comment"),
    path("delete/<int:comment_id>/", delete_comment, name="delete_comment"),
]