from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.models import Project


class IndexView(TemplateView):
    template_name = 'core/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.all()
        context['labels'] = list(projects.values_list('name', flat=True))
        context['budgets'] = list(projects.values_list('budget', flat=True))

        current = Project.objects.filter(status='current')
        upcoming = Project.objects.filter(status='upcoming')
        finished = Project.objects.filter(status='finished')

        context['status_projects'] = [
            ('Current', current),
            ('Finished', finished),
            ('Upcoming', upcoming),
        ]
        return context