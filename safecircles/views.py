from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import SafeCircle, SafeCirclePost, CheckIn, SafeCircleMembership, Report, ReportPhoto, Comment
from .forms import SafeCircleForm, SafeCirclePostForm, CheckInForm, JoinSafeCircleForm, ReportForm, ReportPhotoForm, CommentForm
from django.utils import timezone

def home(request):
    """View for the safecircles home page"""
    if not request.user.is_authenticated:
        return render(request, 'safecircles/landing.html')
    
    user_circles = SafeCircle.objects.filter(members=request.user)
    public_circles = SafeCircle.objects.filter(is_public=True).exclude(members=request.user)
    
    context = {
        'user_circles': user_circles,
        'public_circles': public_circles,
    }
    return render(request, 'safecircles/home.html', context)

@login_required
def create_safecircle(request):
    """View to create a new safecircle"""
    if request.method == 'POST':
        form = SafeCircleForm(request.POST)
        if form.is_valid():
            safecircle = form.save(commit=False)
            safecircle.created_by = request.user
            safecircle.save()
            
            # Create membership with admin role
            SafeCircleMembership.objects.create(
                safecircle=safecircle,
                user=request.user,
                role='admin'
            )
            
            messages.success(request, _('SafeCircle created successfully!'))
            return redirect('safecircles:circle_detail', circle_id=safecircle.id)
    else:
        form = SafeCircleForm()
    
    context = {
        'form': form,
        'map_center': {'lat': 0, 'lng': 0},  # Default to center of the world
    }
    return render(request, 'safecircles/create_safecircle.html', context)

@login_required
def join_safecircle(request):
    """View to join an existing safecircle"""
    if request.method == 'POST':
        form = JoinSafeCircleForm(request.POST)
        if form.is_valid():
            join_code = form.cleaned_data['join_code']
            try:
                safecircle = SafeCircle.objects.get(join_code=join_code)
                if request.user not in safecircle.members.all():
                    SafeCircleMembership.objects.create(
                        safecircle=safecircle,
                        user=request.user,
                        role='member'
                    )
                    messages.success(request, _('Successfully joined %(name)s!') % {'name': safecircle.name})
                    return redirect('safecircles:circle_detail', circle_id=safecircle.id)
                else:
                    messages.warning(request, _('You are already a member of this SafeCircle.'))
            except SafeCircle.DoesNotExist:
                messages.error(request, _('Invalid join code.'))
    else:
        form = JoinSafeCircleForm()
    
    return render(request, 'safecircles/join_safecircle.html', {'form': form})

@login_required
def circle_detail(request, circle_id):
    """View to show details of a specific safecircle"""
    safecircle = get_object_or_404(SafeCircle, id=circle_id)
    membership = SafeCircleMembership.objects.filter(safecircle=safecircle, user=request.user).first()
    
    if not membership and not safecircle.is_public:
        messages.error(request, _('You are not a member of this SafeCircle.'))
        return redirect('safecircles:home')
    
    posts = SafeCirclePost.objects.filter(safecircle=safecircle)
    recent_check_ins = CheckIn.objects.filter(membership__safecircle=safecircle).order_by('-timestamp')[:5]
    
    context = {
        'safecircle': safecircle,
        'membership': membership,
        'posts': posts,
        'recent_check_ins': recent_check_ins,
        'map_center': {
            'lat': float(safecircle.latitude) if safecircle.latitude else -25.9312,
            'lng': float(safecircle.longitude) if safecircle.longitude else 28.0244,
        },
    }
    return render(request, 'safecircles/circle_detail.html', context)

@login_required
def create_post(request, circle_id):
    """View to create a new post in a safecircle"""
    safecircle = get_object_or_404(SafeCircle, id=circle_id)
    membership = SafeCircleMembership.objects.filter(safecircle=safecircle, user=request.user).first()
    
    if not membership:
        messages.error(request, _('You are not a member of this SafeCircle.'))
        return redirect('safecircles:home')
    
    if request.method == 'POST':
        form = SafeCirclePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.safecircle = safecircle
            post.author = request.user
            post.save()
            messages.success(request, _('Post created successfully!'))
            return redirect('safecircles:circle_detail', circle_id=circle_id)
    else:
        form = SafeCirclePostForm()
    
    context = {
        'form': form,
        'safecircle': safecircle,
    }
    return render(request, 'safecircles/create_post.html', context)

@login_required
def check_in(request, circle_id):
    """View for members to check in to a safecircle"""
    safecircle = get_object_or_404(SafeCircle, id=circle_id)
    membership = SafeCircleMembership.objects.filter(safecircle=safecircle, user=request.user).first()
    
    if not membership:
        messages.error(request, _('You are not a member of this SafeCircle.'))
        return redirect('safecircles:home')
    
    if request.method == 'POST':
        form = CheckInForm(request.POST)
        if form.is_valid():
            check_in = form.save(commit=False)
            check_in.membership = membership
            check_in.save()
            
            # Update last check-in time
            membership.last_check_in = check_in.timestamp
            membership.save()
            
            messages.success(request, _('Check-in successful!'))
            return redirect('safecircles:circle_detail', circle_id=circle_id)
    else:
        form = CheckInForm()
    
    context = {
        'form': form,
        'safecircle': safecircle,
        'map_center': {
            'lat': float(safecircle.latitude) if safecircle.latitude else -25.9312,
            'lng': float(safecircle.longitude) if safecircle.longitude else 28.0244,
        },
    }
    return render(request, 'safecircles/check_in.html', context)

@login_required
def circle_members(request, circle_id):
    """View to show members of a safecircle"""
    safecircle = get_object_or_404(SafeCircle, id=circle_id)
    membership = SafeCircleMembership.objects.filter(safecircle=safecircle, user=request.user).first()
    
    if not membership and not safecircle.is_public:
        messages.error(request, _('You are not a member of this SafeCircle.'))
        return redirect('safecircles:home')
    
    members = SafeCircleMembership.objects.filter(safecircle=safecircle, is_active=True)
    
    context = {
        'safecircle': safecircle,
        'members': members,
        'user_membership': membership,
    }
    return render(request, 'safecircles/circle_members.html', context)

@login_required
def manage_member(request, circle_id, user_id):
    """View to manage member roles and status"""
    safecircle = get_object_or_404(SafeCircle, id=circle_id)
    user_membership = SafeCircleMembership.objects.filter(safecircle=safecircle, user=request.user).first()
    target_membership = get_object_or_404(SafeCircleMembership, safecircle=safecircle, user_id=user_id)
    
    if not user_membership or user_membership.role not in ['admin', 'moderator']:
        messages.error(request, _('You do not have permission to manage members.'))
        return redirect('safecircles:circle_members', circle_id=circle_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'promote' and user_membership.role == 'admin':
            target_membership.role = 'moderator'
            target_membership.save()
            messages.success(request, _('Member promoted to moderator.'))
        elif action == 'demote' and user_membership.role == 'admin':
            target_membership.role = 'member'
            target_membership.save()
            messages.success(request, _('Member demoted to regular member.'))
        elif action == 'remove':
            target_membership.is_active = False
            target_membership.save()
            messages.success(request, _('Member removed from SafeCircle.'))
        
        return redirect('safecircles:circle_members', circle_id=circle_id)
    
    context = {
        'safecircle': safecircle,
        'target_membership': target_membership,
        'user_membership': user_membership,
    }
    return render(request, 'safecircles/manage_member.html', context)

@login_required
def report_list(request):
    reports = Report.objects.all().order_by('-created_at')
    
    # Filtering
    status = request.GET.get('status')
    report_type = request.GET.get('type')
    date = request.GET.get('date')
    
    if status:
        reports = reports.filter(status=status)
    if report_type:
        reports = reports.filter(report_type=report_type)
    if date:
        if date == 'today':
            reports = reports.filter(created_at__date=timezone.now().date())
        elif date == 'week':
            reports = reports.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7))
        elif date == 'month':
            reports = reports.filter(created_at__gte=timezone.now() - timezone.timedelta(days=30))
    
    # Pagination
    paginator = Paginator(reports, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'safecircles/report_list.html', {
        'reports': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
    })

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    related_reports = Report.objects.filter(
        Q(latitude__range=(report.latitude-0.01, report.latitude+0.01)) |
        Q(longitude__range=(report.longitude-0.01, report.longitude+0.01))
    ).exclude(id=report_id)[:5]
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.report = report
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('safecircles:report_detail', report_id=report.id)
    else:
        form = CommentForm()
    
    return render(request, 'safecircles/report_detail.html', {
        'report': report,
        'related_reports': related_reports,
        'form': form,
    })

@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, 'Report created successfully.')
            return redirect('safecircles:report_detail', report_id=report.id)
    else:
        form = ReportForm()
    
    return render(request, 'safecircles/create_report.html', {'form': form})

@login_required
def edit_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if report.user != request.user:
        messages.error(request, 'You do not have permission to edit this report.')
        return redirect('safecircles:report_detail', report_id=report.id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully.')
            return redirect('safecircles:report_detail', report_id=report.id)
    else:
        form = ReportForm(instance=report)
    
    return render(request, 'safecircles/edit_report.html', {'form': form, 'report': report})

@login_required
def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if report.user != request.user:
        messages.error(request, 'You do not have permission to delete this report.')
        return redirect('safecircles:report_detail', report_id=report.id)
    
    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted successfully.')
        return redirect('safecircles:report_list')
    
    return render(request, 'safecircles/delete_report.html', {'report': report})

@login_required
def add_photo(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if report.user != request.user:
        messages.error(request, 'You do not have permission to add photos to this report.')
        return redirect('safecircles:report_detail', report_id=report.id)
    
    if request.method == 'POST':
        form = ReportPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.report = report
            photo.save()
            messages.success(request, 'Photo added successfully.')
            return redirect('safecircles:report_detail', report_id=report.id)
    else:
        form = ReportPhotoForm()
    
    return render(request, 'safecircles/add_photo.html', {'form': form, 'report': report})

# Create your views here.
