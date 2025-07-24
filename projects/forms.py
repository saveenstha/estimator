from django import forms
from .models import Project

class ProjectAnalysisForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'client', 'location', 'owner', 'engineer', 'report_date', 'budget']
