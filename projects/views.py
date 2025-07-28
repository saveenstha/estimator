from django.views.generic import View, ListView, DetailView,  CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render

from .models import Project, Drawing
from .forms import ProjectAnalysisForm

from estimates.models import EstimateComponent
from PIL import Image
import pytesseract
import re
from decimal import Decimal


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        components = EstimateComponent.objects.filter(project=self.object)
        context['components'] = components
        context['total_cost'] = sum(c.cost for c in components)
        context['profit_margin'] = ((self.object.budget - context['total_cost']) / self.object.budget *
                                    100) if self.object.budget else 0
        context['per_floor_costs'] = [
            {'floor': i, 'cost': sum(c.cost for c in components.filter(floor_number=i))}
            for i in range(1, self.object.number_of_storeys + 1)
        ]
        return context

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields = ['name', 'client', 'budget','number_of_storeys']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['name', 'client', 'budget','number_of_storeys']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project-list')

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')



class DrawingOCRView(View):
    template_name = 'projects/drawing_ocr_result.html'

    def get(self, request, pk):
        drawing = get_object_or_404(Drawing, pk=pk)
        file_path = drawing.file.path
        try:
            text = pytesseract.image_to_string(Image.open(file_path))
            parsed_components = []

            # Enhanced parsing logic for structural components
            patterns = {
                'concrete': r'Concrete Grade:?\s*M(\d+)',  # e.g., M20
                'steel': r'Steel Grade:?\s*Fe\s*(\d+)',  # e.g., Fe 500
                'column': r'Column:?\s*(\d+x\d+)\s*mm',  # e.g., 350x350
                'beam': r'(?:Main Beam|Plinth Beam):?\s*(\d+x\d+)\s*mm',  # e.g., 225x425
                'slab': r'Slab:?\s*(\d+)\s*mm',  # e.g., 125 mm
                'footing': r'Footing.*?(\d+\.\d+x\d+\.\d+)\s*m',  # e.g., 2.13x2.13 m
                'quantity': r'(\w+):?\s*(\d+\.?\d*)\s*(sq\.ft\.|m|mm|kN)',  # e.g., Plinth Area: 946 sq.ft.
            }

            for key, pattern in patterns.items():
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if key in ['concrete', 'steel']:
                        material, created = Material.objects.get_or_create(
                            name=f"{key.capitalize()} ({match})",
                            defaults={'unit': 'm³' if key == 'concrete' else 'kg', 'rate': 0, 'grade': match}
                        )
                        parsed_components.append({'name': material.name, 'quantity': 0})
                    elif key in ['column', 'beam', 'slab', 'footing']:
                        parsed_components.append({'name': key.capitalize(), 'quantity': 1, 'description': f"Size: {match}"})
                    elif key == 'quantity':
                        name, qty, unit = match
                        parsed_components.append({'name': name, 'quantity': float(qty), 'unit': unit})

            # Auto-create EstimateComponents
            project = drawing.project
            for comp in parsed_components:
                if comp['quantity'] > 0:
                    material, _ = Material.objects.get_or_create(
                        name=comp['name'],
                        defaults={'unit': comp.get('unit', 'unit'), 'rate': 0}
                    )
                    EstimateComponent.objects.get_or_create(
                        project=project,
                        floor_number=1,  # Default to floor 1, can be updated manually
                        material=material,
                        quantity=Decimal(comp['quantity']),
                        defaults={'description': comp.get('description', '')}
                    )

            return render(request, self.template_name, {
                'drawing': drawing,
                'parsed_components': parsed_components,
                'raw_text': text
            })

        except Exception as e:
            return render(request, self.template_name, {
                'drawing': drawing,
                'error': str(e),
                'parsed_components': [],
                'raw_text': ''
            })


class ProjectAnalysisCreateView(CreateView):
    template_name = 'projects/project_analysis_form.html'
    form_class = ProjectAnalysisForm
    success_url = reverse_lazy('project-list')