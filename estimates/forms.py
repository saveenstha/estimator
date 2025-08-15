from django import forms
from .models import EstimateComponent, Material, Procurement, MaterialCategory
from projects.models import Project
import csv
import io

class EstimateComponentForm(forms.ModelForm):
    class Meta:
        model = EstimateComponent
        fields = ['project', 'floor_number', 'material', 'quantity', 'description', 'unit', 'rate',
                  'labor_cost', 'overhead_cost']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'labor_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'overhead_cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        material = cleaned_data.get('material')
        if material and material.grade == 'M20' and material.standard == 'NBC 105:2020':
            if 'Column' in material.name and cleaned_data.get('description', '').find('350x350') == -1:
                raise forms.ValidationError("Column size must be at least 350x350 mm per NBC 105:2020.")
        return cleaned_data

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'unit', 'rate', 'category', 'grade', 'standard']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'standard': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProcurementForm(forms.ModelForm):
    class Meta:
        model = Procurement
        fields = ['project', 'material', 'quantity_required', 'quantity_procured', 'date_procured', 'supplier',
                  'cost', 'due_date']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-control'}),
            'quantity_required': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity_procured': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_procured': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EstimateCSVUploadForm(forms.Form):
    csv_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}))

class FloorEstimateForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    floor_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    materials = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    quantities = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    descriptions = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        quantities = cleaned_data.get('quantities')
        materials = cleaned_data.get('materials')
        floor_number = cleaned_data.get('floor_number')
        project = cleaned_data.get('project')

        if quantities and materials:
            qty_list = [float(q) for q in quantities.split(',') if q.strip()]
            if len(qty_list) != len(materials):
                raise forms.ValidationError("Number of quantities must match number of materials selected.")
        if floor_number and project and floor_number > project.number_of_storeys:
            raise forms.ValidationError("Floor number exceeds project's number of storeys.")
        return cleaned_data