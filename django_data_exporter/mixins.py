import csv
from django.http import StreamingHttpResponse

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

class DataExporterMixin:
    filename = "export"
    
    def get_filename(self):
        return f"{self.filename}.csv"

    def get_header(self):
        """Return a list of strings for the header row."""
        raise NotImplementedError("Subclasses must implement get_header()")

    def get_queryset(self):
        """Return the queryset of objects to export."""
        raise NotImplementedError("Subclasses must implement get_queryset()")

    def format_row(self, obj):
        """Return a list of strings representing the row for the given object."""
        raise NotImplementedError("Subclasses must implement format_row()")

    def csv_generator(self, header, queryset):
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer, delimiter=';', lineterminator='\n')

        # BOM for Excel to understand UTF-8
        yield '\ufeff'

        # Yield header
        yield writer.writerow(header)

        # Iterate and format each object
        for obj in queryset:
            yield writer.writerow(self.format_row(obj))
