from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CrimeReport(models.Model):
    CRIME_TYPES = [
        ('theft', _('Theft')),
        ('burglary', _('Burglary')),
        ('assault', _('Assault')),
        ('vandalism', _('Vandalism')),
        ('other', _('Other')),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='crime_reports'
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    type = models.CharField(max_length=20, choices=CRIME_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    media_file = models.FileField(
        upload_to='crime_reports/',
        blank=True,
        null=True,
        help_text=_('Upload a photo or audio file related to the incident')
    )
    is_verified = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('Pending')),
            ('investigating', _('Investigating')),
            ('resolved', _('Resolved')),
            ('false_report', _('False Report')),
        ],
        default='pending'
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_type_display()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class EmergencyAlert(models.Model):
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='emergency_alerts'
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)
    handled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='handled_alerts'
    )
    handled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Emergency Alert at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
