import csv
import io
from django.http import HttpResponse, StreamingHttpResponse
from django.template.loader import render_to_string

# We try to import optional dependencies
try:
    from openpyxl import Workbook
except ImportError:
    Workbook = None

try:
    from weasyprint import HTML
except ImportError:
    HTML = None

class ExportService:
    @staticmethod
    def to_csv(filename, header, queryset, format_row_func):
        class Echo:
            def write(self, value):
                return value

        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer, delimiter=';', lineterminator='\n')

        def generator():
            yield '\ufeff'  # BOM
            yield writer.writerow(header)
            for obj in queryset:
                yield writer.writerow(format_row_func(obj))

        response = StreamingHttpResponse(generator(), content_type="text/csv; charset=utf-8")
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        return response

    @staticmethod
    def to_xlsx(filename, header, queryset, format_row_func):
        if Workbook is None:
            return HttpResponse("openpyxl is not installed.", status=501)

        wb = Workbook()
        ws = wb.active
        ws.append(header)

        for obj in queryset:
            ws.append(format_row_func(obj))

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        return response

    @staticmethod
    def to_pdf(filename, header, queryset, format_row_func, template_name='django_data_exporter/pdf_template.html'):
        if HTML is None:
            return HttpResponse("weasyprint is not installed.", status=501)

        data = [format_row_func(obj) for obj in queryset]
        html_string = render_to_string(template_name, {
            'header': header,
            'data': data,
            'title': filename
        })
        
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
        return response
