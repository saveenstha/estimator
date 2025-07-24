from django import forms
from .models import EstimateComponent, Material, Procurement, MaterialCategory


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'unit', 'rate', 'category']


class ProcurementForm(forms.ModelForm):
    class Meta:
        model = Procurement
        fields = [
            'project', 'material', 'quantity_required', 'quantity_procured',
            'date_procured', 'supplier', 'cost'
        ]


class EstimateComponentForm(forms.ModelForm):
    class Meta:
        model = EstimateComponent
        fields = ['project', 'floor_number', 'material', 'quantity']


class FloorEstimateForm(forms.ModelForm):
    class Meta:
        model = EstimateComponent
        fields = ['project', 'floor_number', 'description', 'material', 'quantity', 'unit', 'rate']


class EstimateCSVUploadForm(forms.Form):
    csv_file = forms.FileField()