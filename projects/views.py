from django.views.generic import View, ListView, DetailView,  CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render

from .models import Project, Drawing
from .forms import ProjectAnalysisForm

from estimates.models import EstimateComponent
from PIL import Image
import pytesseract


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



class DrawingOCRView(View):
    template_name = 'projects/drawing_ocr_result.html'

    def get(self, request, pk):
        drawing = get_object_or_404(Drawing, pk=pk)
        file_path = drawing.file.path
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)

            # Example parser logic
            parsed_components = []
            for line in text.splitlines():
                if ':' in line:
                    name, qty = line.split(':', 1)
                    name = name.strip()
                    try:
                        quantity = float(qty.strip().split()[0])
                        parsed_components.append({'name': name, 'quantity': quantity})
                    except:
                        continue

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