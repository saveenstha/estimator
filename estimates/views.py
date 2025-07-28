from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView, FormView, View
)
from django.urls import reverse_lazy
from  django.shortcuts import get_object_or_404, render
from .models import EstimateComponent, Material, MaterialCategory, Procurement

from .forms import (
    EstimateComponentForm, EstimateCSVUploadForm,
    MaterialForm, ProcurementForm, FloorEstimateForm
)
from projects.models import Project
from django.http import HttpResponse
import csv
import io

# Material CRUD

class MaterialListView(ListView):
    model = Material
    template_name = 'estimates/material_list.html'
    context_object_name = 'materials'
    paginate_by = 10

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            return Material.objects.filter(category__name=category)
        return Material.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = MaterialCategory.objects.all()
        return context

class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'estimates/material_form.html'
    success_url = reverse_lazy('material-list')


class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'estimates/material_form.html'
    success_url = reverse_lazy('material-list')

class MaterialDeleteView(DeleteView):
    model = Material
    template_name = 'estimates/material_confirm_delete.html'
    success_url = reverse_lazy('material-list')


# Estimates CRUD
class EstimateListView(ListView):
    model = EstimateComponent
    template_name = 'estimates/estimate_list.html'
    context_object_name = 'estimates'

    def get_queryset(self):
        queryset = super().get_queryset()
        project_id = self.request.GET.get('project')
        material_id = self.request.GET.get('material')

        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if material_id:
            queryset = queryset.filter(material_id=material_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['materials'] = Material.objects.all()
        context['selected_project'] = self.request.GET.get('project')
        context['selected_material'] = self.request.GET.get('material')
        return context

class EstimateDetailView(DetailView):
    model = EstimateComponent
    template_name = 'estimates/estimate_detail.html'
    context_object_name = 'estimate'

class EstimateCreateView(CreateView):
    model = EstimateComponent
    form_class = EstimateComponentForm
    template_name = 'estimates/estimate_form.html'
    success_url = reverse_lazy('estimate-list')

class EstimateUpdateView(UpdateView):
    model = EstimateComponent
    form_class = EstimateComponentForm
    template_name = 'estimates/estimate_form.html'
    success_url = reverse_lazy('estimate-list')

class EstimateDeleteView(DeleteView):
    model = EstimateComponent
    template_name = 'estimates/estimate_confirm_delete.html'
    success_url = reverse_lazy('estimate-list')

# CSV upload

class EstimateCSVUploadView(FormView):
    template_name = 'estimates/upload_csv.html'
    form_class = EstimateCSVUploadForm
    success_url = reverse_lazy('project-list')

    def form_valid(self, form):
        csv_file = form.cleaned_data['csv_file']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        next(io_string)

        for row in csv.reader(io_string):
            try:
                project_id, floor_number, material_name, quantity = row
                project = Project.objects.get(id=project_id)
                material = Material.objects.get(name=material_name)
                EstimateComponent.objects.create(
                    project=project,
                    floor_number=int(floor_number),
                    material=material,
                    quantity=float(quantity)
                )
            except Exception as e:
                continue
        return super().form_valid(form)

# FLOOR ESTIMATE (Detailed Manual Entry)
# ------------------------------------------------------------
class FloorEstimateCreateView(CreateView):
    template_name = 'estimates/floor_estimate_form.html'
    form_class = FloorEstimateForm
    success_url = reverse_lazy('project-list')

# PROCUREMENT VIEWS
# ------------------------------------------------------------
class ProcurementListView(ListView):
    model = Procurement
    template_name = 'estimates/procurement_list.html'
    context_object_name = 'procurements'


class ProcurementDetailView(DetailView):
    model = Procurement
    template_name = 'estimates/procurement_detail.html'


class ProcurementCreateView(CreateView):
    model = Procurement
    form_class = ProcurementForm
    template_name = 'estimates/procurement_form.html'
    success_url = reverse_lazy('procurement-list')


class ProcurementUpdateView(UpdateView):
    model = Procurement
    form_class = ProcurementForm
    template_name = 'estimates/procurement_form.html'
    success_url = reverse_lazy('procurement-list')


class ProcurementDeleteView(DeleteView):
    model = Procurement
    template_name = 'estimates/procurement_confirm_delete.html'
    success_url = reverse_lazy('procurement-list')


class CostReportView(View):
    template_name = 'estimates/cost_report.html'

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        components = EstimateComponent.objects.filter(project=project)
        per_floor_costs = [
            {
                'floor': i,
                'cost': sum(c.cost for c in components.filter(floor_number=i)),
                'materials': [
                    {'name': c.material.name, 'quantity': c.quantity, 'cost': c.cost}
                    for c in components.filter(floor_number=i)
                ]
            }
            for i in range(1, project.number_of_storeys + 1)
        ]
        total_cost = sum(c.cost for c in components)
        profit_margin = ((project.budget - total_cost) / project.budget * 100) if project.budget else 0

        # Chart data
        labels = [f"Floor {i}" for i in range(1, project.number_of_storeys + 1)]
        costs = [pc['cost'] for pc in per_floor_costs]

        return render(request, self.template_name, {
            'project': project,
            'per_floor_costs': per_floor_costs,
            'total_cost': total_cost,
            'profit_margin': profit_margin,
            'labels': labels,
            'costs': costs
        })
