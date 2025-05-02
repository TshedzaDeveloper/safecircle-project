from django import template
from ..models import Notification

register = template.Library()

@register.simple_tag
def get_unread_notification_count(user):
    """Returns the count of unread notifications for a user"""
    return Notification.objects.filter(user=user, is_read=False).count() 