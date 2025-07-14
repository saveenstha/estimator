from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Drawing(models.Model):
    DRAWING_TYPES = [
        ('architectural', 'Architectural'),
        ('structural', 'Structural')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(choices=DRAWING_TYPES, max_length=20)
    file = models.FileField(upload_to='drawings/')

    def __str__(self):
        return f"{self.project.name} - {self.type}"