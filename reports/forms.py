from django import forms
from .models import CrimeReport, EmergencyAlert
from django.utils.translation import gettext_lazy as _

class CrimeReportForm(forms.ModelForm):
    class Meta:
        model = CrimeReport
        fields = ['type', 'description', 'latitude', 'longitude', 'is_anonymous', 'media_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'media_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*,audio/*'}),
        }
        labels = {
            'type': _('Type of Crime'),
            'description': _('Description of the Incident'),
            'is_anonymous': _('Report Anonymously'),
            'media_file': _('Upload Evidence (Photo/Audio)'),
        }

class EmergencyAlertForm(forms.ModelForm):
    class Meta:
        model = EmergencyAlert
        fields = ['latitude', 'longitude']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        } 