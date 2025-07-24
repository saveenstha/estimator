from django.db import models
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.models import Project
from estimates.models import Procurement

class IndexView(TemplateView):
    template_name = 'core/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.all()
        procurements = Procurement.objects.all()

        context['labels'] = list(projects.values_list('name', flat=True))
        context['budgets'] = list(projects.values_list('budget', flat=True))

        current = Project.objects.filter(status='current')
        upcoming = Project.objects.filter(status='upcoming')
        finished = Project.objects.filter(status='finished')

        context['total_procurements'] = procurements.count()
        context['fulfilled'] = procurements.filter(quantity_procured__gte=models.F('quantity_required')).count()
        context['pending'] = procurements.filter(quantity_procured__lt=models.F('quantity_required')).count()


        context['status_projects'] = [
            ('Current', current),
            ('Finished', finished),
            ('Upcoming', upcoming),
        ]
        return context