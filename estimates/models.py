from django.db import models
from projects.models import Project


class MaterialCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True)  # e.g., M20 for concrete, Fe 500 for steel
    standard = models.CharField(max_length=100, blank=True)  # e.g., NBC 105:2020

    def __str__(self):
        return self.name

class EstimateComponent(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    floor_number = models.IntegerField()
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)  # Add detailed description of work
    unit = models.CharField(max_length=50, default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # New field for labor cost
    overhead_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # New field for overheads

    @property
    def cost(self):
        return self.quantity * self.rate + self.labor_cost + self.overhead_cost

    def __str__(self):
        return f"{self.project.name} - Floor {self.floor_number} - {self.material.name}"


class Procurement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_required = models.FloatField()
    quantity_procured = models.FloatField(default=0)
    date_procured = models.DateField(null=True, blank=True)
    supplier = models.CharField(max_length=255, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_date = models.DateField(null=True, blank=True, help_text="Date by which procurement must be completed.")

    def progress_percent(self):
        if self.quantity_required == 0:
            return 100
        return min(100, round((self.quantity_procured / self.quantity_required) * 100))

    def is_urgent(self):
        from django.utils import timezone
        if not self.due_date:
            return False
        return self.quantity_procured < self.quantity_required and self.due_date <= timezone.now().date()

    def is_fulfilled(self):
        return self.quantity_procured >= self.quantity_required

    def __str__(self):
        return f"{self.project.name} - {self.material.name}"