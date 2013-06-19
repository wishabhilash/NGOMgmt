from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *
from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('project_name', 'assigned_to', 'outsourced_from', 'project_leader')

admin.site.register(Project, ProjectAdmin)



class ProjectProgressAdmin(admin.ModelAdmin):
	pass

admin.site.register(ProjectProgress, ProjectProgressAdmin)



		