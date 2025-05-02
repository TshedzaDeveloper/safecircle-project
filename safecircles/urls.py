from django.urls import path
from . import views

app_name = 'safecircles'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_safecircle, name='create_safecircle'),
    path('join/', views.join_safecircle, name='join_safecircle'),
    path('<int:circle_id>/', views.circle_detail, name='circle_detail'),
    path('<int:circle_id>/create-post/', views.create_post, name='create_post'),
    path('<int:circle_id>/check-in/', views.check_in, name='check_in'),
    path('<int:circle_id>/members/', views.circle_members, name='circle_members'),
    path('<int:circle_id>/members/<int:user_id>/manage/', views.manage_member, name='manage_member'),
] 