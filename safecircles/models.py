from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import User
from django.utils import timezone

class SafeCircle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location_area = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    radius = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, help_text=_('Radius in kilometers'))
    join_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='safecircles',
        through='SafeCircleMembership'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_safecircles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False, help_text=_('Whether the SafeCircle is visible to non-members'))

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_member_count(self):
        return self.members.count()

    def get_active_members(self):
        return self.members.filter(safecirclemembership__is_active=True)

class SafeCircleMembership(models.Model):
    ROLES = [
        ('admin', _('Admin')),
        ('moderator', _('Moderator')),
        ('member', _('Member')),
    ]

    safecircle = models.ForeignKey(SafeCircle, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    last_check_in = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('safecircle', 'user')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.email} in {self.safecircle.name}"

class SafeCirclePost(models.Model):
    POST_TYPES = [
        ('announcement', _('Announcement')),
        ('alert', _('Alert')),
        ('update', _('Update')),
        ('general', _('General')),
    ]

    safecircle = models.ForeignKey(
        SafeCircle,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='safecircle_posts'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='general')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', '-is_urgent', '-created_at']

    def __str__(self):
        return self.title

class CheckIn(models.Model):
    membership = models.ForeignKey(SafeCircleMembership, on_delete=models.CASCADE, related_name='check_ins')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('safe', _('Safe')),
            ('concerned', _('Concerned')),
            ('emergency', _('Emergency')),
        ],
        default='safe'
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Check-in by {self.membership.user.username} at {self.timestamp}"

class Report(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    TYPE_CHOICES = [
        ('emergency', 'Emergency'),
        ('suspicious', 'Suspicious Activity'),
        ('general', 'General'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_description = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ReportPhoto(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='photos')
    image = models.FileField(upload_to='report_photos/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Photo for {self.report.title}"

class Comment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.report.title}"
