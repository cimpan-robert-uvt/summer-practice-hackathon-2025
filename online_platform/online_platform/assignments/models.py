from django.db import models
from django.conf import settings
from users.admin import CustomUser

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assignments_created_tasks")


    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to="assignments_files/", blank=True, null=True)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)  # <== Nou

    STATUS_CHOICES = [
        ('pending', 'În așteptare'),
        ('approved', 'Aprobată'),
        ('rejected', 'Respinsă'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approval_comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.student.username}"
