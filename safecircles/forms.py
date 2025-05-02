from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import SafeCircle, SafeCirclePost, CheckIn, Report, ReportPhoto, Comment
from core.models import UserProfile

class SafeCircleForm(forms.ModelForm):
    class Meta:
        model = SafeCircle
        fields = ['name', 'description', 'location_area', 'latitude', 'longitude', 'radius', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location_area': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'radius': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': _('SafeCircle Name'),
            'description': _('Description'),
            'location_area': _('Location Area'),
            'radius': _('Radius (km)'),
            'is_public': _('Make Public'),
        }

class SafeCirclePostForm(forms.ModelForm):
    class Meta:
        model = SafeCirclePost
        fields = ['title', 'content', 'post_type', 'is_urgent', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'is_urgent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': _('Title'),
            'content': _('Content'),
            'post_type': _('Type'),
            'is_urgent': _('Urgent'),
            'is_pinned': _('Pin to Top'),
        }

class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = ['status', 'notes', 'latitude', 'longitude']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': _('Optional notes about your status...')}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }
        labels = {
            'status': _('How are you?'),
            'notes': _('Additional Information'),
        }

class JoinSafeCircleForm(forms.Form):
    join_code = forms.UUIDField(
        label=_('Join Code'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter the SafeCircle join code')})
    )

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'report_type', 'latitude', 'longitude', 'location_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'report_type': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'location_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReportPhotoForm(forms.ModelForm):
    class Meta:
        model = ReportPhoto
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 