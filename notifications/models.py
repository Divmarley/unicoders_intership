from django.db import models
from accounts.models import User


NOTIFICATION_TYPE = (
    (1, "Application"),
    (2, "Staff Notication")
)

class Notification(models.Model):
    to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    notification_type = models.IntegerField(default=0, choices=NOTIFICATION_TYPE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_notifications', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
