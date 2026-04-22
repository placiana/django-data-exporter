# EXAMPLE OF INTEGRATION

# 1. In your models.py:
# from django.db import models
# class Project(models.Model):
#     name = models.CharField(max_length=100)
#     client = models.CharField(max_length=100)
#     budget = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

# 2. In your views.py:
from django_data_exporter.views import BaseDataExportView
# from .models import Project

class ProjectExportView(BaseDataExportView):
    # model = Project  # Generic ListView needs a model or queryset
    filename = "reporte_proyectos"

    def get_queryset(self):
        # return Project.objects.all()
        return [] # Mock for example

    def get_header(self):
        return ["ID", "Nombre del Proyecto", "Cliente", "Presupuesto", "Fecha de Creación"]

    def format_row(self, obj):
        return [
            str(obj.id),
            obj.name,
            obj.client,
            f"${obj.budget}",
            obj.created_at.strftime("%Y-%m-%d %H:%M")
        ]

# 3. In your urls.py:
# from django.urls import path
# from .views import ProjectExportView

# urlpatterns = [
#     path('proyectos/exportar/', ProjectExportView.as_view(), name='project_export'),
# ]
