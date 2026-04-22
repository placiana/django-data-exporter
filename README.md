# Django Data Exporter

Una app de Django reutilizable para previsualizar y exportar datos en múltiples formatos.

## Requerimientos
- Django
- openpyxl (opcional, para XLSX)
- django-weasyprint (opcional, para PDF)

## Instalación

Puedes instalarlo directamente desde el repositorio de Git:

```bash
pip install git+https://github.com/placiana/django-data-exporter.git
```

O agregarlo a tu `requirements.txt`:
```text
django-data-exporter @ git+https://github.com/placiana/django-data-exporter.git
```

Si necesitas soporte para Excel o PDF, instala los extras:
```bash
pip install "django-data-exporter[xlsx,pdf] @ git+https://github.com/placiana/django-data-exporter.git"
```

Luego, agrega `django_data_exporter` a `INSTALLED_APPS` en tu `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'django_data_exporter',
]
```

## Uso
Hereda de `BaseDataExportView` y define los métodos necesarios:

```python
from django_data_exporter.views import BaseDataExportView

class MiExportacionView(BaseDataExportView):
    filename = "mis_datos"

    def get_queryset(self):
        return MiModelo.objects.all()

    def get_header(self):
        return ["Columna 1", "Columna 2"]

    def format_row(self, obj):
        return [obj.campo1, obj.campo2]
```

En tu `urls.py`:
```python
path('exportar/', MiExportacionView.as_view(), name='mi_exportar'),
```

## Características
- **Previsualización**: Muestra una tabla HTML con los primeros 100 registros.
- **Copiar al Portapapeles**: Formato TSV compatible con Excel/Sheets.
- **Formatos soportados**: CSV, XLSX, PDF.
```
