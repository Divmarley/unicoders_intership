from .models import Notification

def create_notification(request, to_user=None, notification_type=None, content=None):
    Notification.objects.create(
        to_user=to_user, 
        notification_type=notification_type, 
        created_by=request.user, 
        content=content
        )