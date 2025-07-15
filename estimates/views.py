from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from .models import EstimateComponent, Material, MaterialCategory, Procurement
from .forms import EstimateComponentForm, EstimateCSVUploadForm, MaterialForm, ProcurementForm
from projects.models import Project

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


# Procurement CRUD
class ProcurementListView(ListView):
    model = Procurement
    template_name = 'estimates/procurement_list.html'
    context_object_name = 'procurements'

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

class ProcurementDetailView(DetailView):
    model = Procurement
    template_name = 'estimates/procurement_detail.html'

# Estimate Component CRUD
class EstimateComponentCreateView(CreateView):
    model = EstimateComponent
    form_class = EstimateComponentForm
    template_name = 'estimates/add_estimate.html'
    success_url = reverse_lazy('project-list')


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
            project_id, floor_number, material_name, quantity = row
            project = Project.objects.get(id=project_id)
            material = Material.objects.get(name=material_name)
            EstimateComponent.objects.create(
                project=project,
                floor_number=int(floor_number),
                material=material,
                quantity=float(quantity)
            )
        return super().form_valid(form)
