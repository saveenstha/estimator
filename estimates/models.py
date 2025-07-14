from django.db import models
from projects.models import Project

class Material(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=10, decimal_places=2)

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
