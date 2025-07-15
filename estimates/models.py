from django.db import models
from projects.models import Project


class MaterialCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class EstimateComponent(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    floor_number = models.IntegerField()
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def cost(self):
        return self.quantity * self.material.rate

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

    def is_fulfilled(self):
        return self.quantity_procured >= self.quantity_required

    def progress_percent(self):
        if self.quantity_required == 0:
            return 0
        return round((self.quantity_procured / self.quantity_required) * 100, 2)

    def __str__(self):
        return f"{self.project.name} - {self.material.name}"