from django.db import models
from app.models import Module
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.conf import settings


class Resource(models.Model):

    RESOURCE_TYPES = (
        ('youtube', 'YouTube'),
        ('website', 'Website'),
        ('textbook', 'Textbook'),
        ('notes', 'Notes'),
    )

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='resources'
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,

    )


    title = models.CharField(max_length=200)

    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES
    )

    link = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    description = models.TextField(blank=True)

    likes = models.ManyToManyField(
        User,
        related_name='liked_resources',
        blank=True
    )
    saved_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='saved_resources',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_flagged = models.BooleanField(default=False)

    def clean(self):
        if self.link and self.file:
            raise ValidationError("Only one resource type allowed")
        if not self.link and not self.file:
            raise ValidationError("Either link or file is required")

    def __str__(self):
        return self.title

class SavedResource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resource')

class Comment(models.Model):
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    is_flagged = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']


