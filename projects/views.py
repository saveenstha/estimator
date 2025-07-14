from django.views.generic import ListView, DetailView,  CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Project
from estimates.models import EstimateComponent

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        components = EstimateComponent.objects.filter(project=self.object)
        context['components'] = components
        context['total_cost'] = sum(c.cost for c in components)
        return context

class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'client', 'budget']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project-list')

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['name', 'client', 'budget']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project-list')

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')