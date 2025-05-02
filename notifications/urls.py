from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:notification_id>/', views.notification_detail, name='notification_detail'),
    path('<int:notification_id>/mark_read/', views.mark_notification_read, name='mark_notification_read'),
    path('mark_all_read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
] 