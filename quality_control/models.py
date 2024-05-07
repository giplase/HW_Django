from django.db import models
from tasks.models import Project, Task


# Create your models here.
class BugReport(models.Model):

    STATUS_CHOICES = [
        ('New', 'Новый'),
        ('In_progress', 'В работе'),
        ('Completed', 'Завершен'),
    ]
    PRIORITY_CHOICES = [
        (1, 'Высокий'),
        (2, 'Средний'),
        (3, 'Низкий'),
    ]

    def __str__(self):
        return self.name

    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(
        Project,
        related_name='bugs',
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        related_name='bugs',
        on_delete=models.SET_NULL,
        null=True,
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='New',
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class FeatureRequest(models.Model):

    STATUS_CHOICES = [
        ('Review', 'Рассмотрение'),
        ('Accepted', 'Принято'),
        ('Rejected', 'Отклонено'),
    ]
    PRIORITY_CHOICES = [
        (1, 'Высокий'),
        (2, 'Средний'),
        (3, 'Низкий'),
    ]


    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(
        Project,
        related_name='requests',
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        related_name='requests',
        on_delete=models.SET_NULL,
        null=True,
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Review',
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
