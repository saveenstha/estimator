from django.views.generic import ListView, DetailView,  CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Project
from estimates.models import EstimateComponent

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
        return context

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    fields = ['name', 'client', 'budget']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['name', 'client', 'budget']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project-list')

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')