from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import CrimeReport, EmergencyAlert
from .forms import CrimeReportForm, EmergencyAlertForm
from django.utils.translation import gettext_lazy as _

# Create your views here.
def report_list(request):
    reports = CrimeReport.objects.all().order_by('-timestamp')
    
    # Filtering
    crime_type = request.GET.get('type')
    if crime_type:
        reports = reports.filter(type=crime_type)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        reports = reports.filter(
            Q(description__icontains=search_query) |
            Q(type__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'reports': page_obj,
        'crime_types': CrimeReport.CRIME_TYPES,
    }
    return render(request, 'reports/report_list.html', context)

@login_required
def create_report(request):
    if request.method == 'POST':
        form = CrimeReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.save()
            messages.success(request, _('Crime report submitted successfully!'))
            return redirect('reports:report_detail', report_id=report.id)
    else:
        form = CrimeReportForm()
    
    context = {
        'form': form,
        'map_center': {'lat': 0, 'lng': 0},  # Default to center of the world
    }
    return render(request, 'reports/create_report.html', context)

def report_detail(request, report_id):
    report = get_object_or_404(CrimeReport, id=report_id)
    context = {
        'report': report,
        'map_center': {'lat': float(report.latitude), 'lng': float(report.longitude)},
    }
    return render(request, 'reports/report_detail.html', context)

@login_required
def edit_report(request, report_id):
    report = get_object_or_404(CrimeReport, id=report_id)
    if report.reporter != request.user and not request.user.is_staff:
        messages.error(request, _('You do not have permission to edit this report.'))
        return redirect('reports:report_detail', report_id=report.id)
    
    if request.method == 'POST':
        form = CrimeReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, _('Report updated successfully!'))
            return redirect('reports:report_detail', report_id=report.id)
    else:
        form = CrimeReportForm(instance=report)
    
    context = {
        'form': form,
        'report': report,
        'map_center': {'lat': float(report.latitude), 'lng': float(report.longitude)},
    }
    return render(request, 'reports/edit_report.html', context)

@login_required
def delete_report(request, report_id):
    report = get_object_or_404(CrimeReport, id=report_id)
    if report.reporter != request.user and not request.user.is_staff:
        messages.error(request, _('You do not have permission to delete this report.'))
        return redirect('reports:report_detail', report_id=report.id)
    
    report.delete()
    messages.success(request, _('Report deleted successfully!'))
    return redirect('reports:report_list')

@login_required
def respond_to_report(request, report_id):
    report = get_object_or_404(CrimeReport, id=report_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(CrimeReport._meta.get_field('status').choices):
            report.status = new_status
            report.save()
            messages.success(request, _('Report status updated successfully!'))
        return redirect('reports:report_detail', report_id=report.id)
    
    context = {
        'report': report,
    }
    return render(request, 'reports/respond_to_report.html', context)

@login_required
def emergency_alert(request):
    if request.method == 'POST':
        form = EmergencyAlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            alert.reporter = request.user
            alert.save()
            messages.success(request, _('Emergency alert sent successfully!'))
            return redirect('core:dashboard')
    else:
        form = EmergencyAlertForm()
    
    context = {
        'form': form,
        'map_center': {'lat': 0, 'lng': 0},  # Default to center of the world
    }
    return render(request, 'reports/emergency_alert.html', context)
