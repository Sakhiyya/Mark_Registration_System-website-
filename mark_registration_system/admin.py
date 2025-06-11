from django.contrib import admin
from .models import MarkEntry

@admin.register(MarkEntry)
class MarkEntryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'module_name', 'date_of_entry', 'gender')
    search_fields = ('student_name', 'module_name', 'student_id')
