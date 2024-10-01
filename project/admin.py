from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('projectname', 'start_date', 'end_date', 'priority', 'status')
    search_fields = ('projectname', 'status')
    list_filter = ('status', 'priority')

admin.site.register(Project, ProjectAdmin)

