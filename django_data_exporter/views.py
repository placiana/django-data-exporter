from django.views.generic import ListView
from django.shortcuts import render
from .mixins import DataExporterMixin
from .utils import ExportService

class BaseDataExportView(DataExporterMixin, ListView):
    template_name = 'django_data_exporter/export_preview.html'
    context_object_name = 'object_list'

    def get(self, request, *args, **kwargs):
        export_format = request.GET.get('export')
        
        if export_format:
            return self.export_data(export_format)
        
        return super().get(request, *args, **kwargs)

    def export_data(self, format):
        header = self.get_header()
        queryset = self.get_queryset()
        filename = self.get_filename().split('.')[0] # Remove extension if any

        if format == 'csv':
            return ExportService.to_csv(filename, header, queryset, self.format_row)
        elif format == 'xlsx':
            return ExportService.to_xlsx(filename, header, queryset, self.format_row)
        elif format == 'pdf':
            return ExportService.to_pdf(filename, header, queryset, self.format_row)
        
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = self.get_header()
        
        # We process rows for preview
        preview_data = []
        for obj in self.get_queryset()[:100]: # Limit preview to 100 rows for performance
            preview_data.append(self.format_row(obj))
        
        context['preview_data'] = preview_data
        context['filename'] = self.get_filename()
        return context
