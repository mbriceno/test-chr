from django.contrib import admin
from .models import Project

class Project_Admin(admin.ModelAdmin):
    list_display = ['external_id', 'name', 'type', 'region', 'typology', 'owner', 'investment', 'date_income', 'status']


admin.site.register(Project, Project_Admin)