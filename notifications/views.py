from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification

@login_required
def notification_list(request):
    """View to list all notifications for the current user"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/notification_list.html', context)

@login_required
def notification_detail(request, notification_id):
    """View to show details of a specific notification"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    
    # Mark the notification as read when viewing
    if not notification.is_read:
        notification.is_read = True
        notification.save()
    
    context = {
        'notification': notification,
    }
    return render(request, 'notifications/notification_detail.html', context)

@login_required
def mark_notification_read(request, notification_id):
    """View to mark a specific notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    
    if not notification.is_read:
        notification.is_read = True
        notification.save()
        messages.success(request, 'Notification marked as read')
    
    return redirect('notifications:notification_list')

@login_required
def mark_all_notifications_read(request):
    """View to mark all notifications as read"""
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    count = unread_notifications.count()
    
    if count > 0:
        unread_notifications.update(is_read=True)
        messages.success(request, f'Marked {count} notifications as read')
    
    return redirect('notifications:notification_list') 