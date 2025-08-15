import json
from django.views.generic import View, TemplateView
from django.shortcuts import render
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from projects.models import Project
from estimates.models import EstimateComponent, Procurement


class IndexView(TemplateView):
    template_name = 'core/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        projects = Project.objects.all()
        status_projects = {
            'Current': projects.filter(status='current'),
            'Finished': projects.filter(status='finished'),
            'Upcoming': projects.filter(status='upcoming')
        }
        total_projects = projects.count()
        total_cost = 0
        profit_margins = []

        for p in projects:
            project_cost = sum(float(c.cost) for c in EstimateComponent.objects.filter(project=p))
            total_cost += project_cost
            if p.budget > 0:
                profit_margin = ((float(p.budget) - project_cost) / float(p.budget) * 100)
                profit_margins.append(profit_margin)

        avg_profit_margin = sum(profit_margins) / len(profit_margins) if profit_margins else 0

        # Procurement Data
        procurements = Procurement.objects.all()
        total_procurements = procurements.count()
        fulfilled = procurements.filter(quantity_procured__gte=models.F('quantity_required')).count()
        pending = total_procurements - fulfilled

        # Urgent procurements (handle missing due_date gracefully)
        urgent_procurements = []
        try:
            for proc in procurements:
                urgency = 'normal'
                if proc.quantity_procured >= proc.quantity_required:
                    urgency = 'completed'
                elif proc.due_date:
                    if proc.due_date < timezone.now().date():
                        urgency = 'overdue'
                    elif proc.due_date <= timezone.now().date() + timedelta(days=7):
                        urgency = 'due-soon'
                urgent_procurements.append({
                    'proc': proc,
                    'progress': proc.progress_percent(),
                    'urgency': urgency
                })
        except AttributeError:
            pass

        # Budget chart data
        labels = [p.name for p in projects]
        budgets = [float(p.budget) for p in projects]

        # Per-floor cost data
        floor_data = {}
        for p in projects:
            components = EstimateComponent.objects.filter(project=p)
            for floor in range(1, p.number_of_storeys + 1):
                floor_cost = sum(c.cost for c in components.filter(floor_number=floor))
                floor_data.setdefault(floor, 0)
                floor_data[floor] += floor_cost

        floor_labels = [f"Floor {f}" for f in sorted(floor_data.keys())]
        floor_costs = [float(floor_data[f]) for f in sorted(floor_data.keys())]

        context = {
            'status_projects': status_projects,
            'total_projects': total_projects,
            'total_cost': total_cost,
            'avg_profit_margin': avg_profit_margin,
            'total_procurements': total_procurements,
            'fulfilled': fulfilled,
            'pending': pending,
            'urgent_procurements': urgent_procurements,
            'labels': json.dumps(labels),
            'budgets': json.dumps(budgets),
            'floor_labels': json.dumps(floor_labels),
            'floor_costs': json.dumps(floor_costs)
        }
        return context