from django import forms
from .models import EstimateComponent, Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'unit', 'rate']


class EstimateComponentForm(forms.ModelForm):
    class Meta:
        model = EstimateComponent
        fields = ['project', 'floor_number', 'material', 'quantity']

class EstimateCSVUploadForm(forms.Form):
    csv_file = forms.FileField()