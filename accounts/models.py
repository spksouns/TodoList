from django.db import models
from django.contrib.auth.models import User

#Database data model
class Task1(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
