from django.db import models
from users.models import CustomUser

class Task(models.Model):
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks_assigned_tasks")
