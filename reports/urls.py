from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('create/', views.create_report, name='create_report'),
    path('<int:report_id>/', views.report_detail, name='report_detail'),
    path('<int:report_id>/edit/', views.edit_report, name='edit_report'),
    path('<int:report_id>/delete/', views.delete_report, name='delete_report'),
    path('<int:report_id>/respond/', views.respond_to_report, name='respond_to_report'),
    path('emergency/', views.emergency_alert, name='emergency_alert'),
] 