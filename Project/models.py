from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Project(models.Model):
	project_name = models.CharField(max_length=200)
	project_description = models.TextField()
	assigned_to = models.CharField(max_length=200)
	outsourced_from = models.CharField(max_length=200)
	project_value = models.BigIntegerField()
	project_leader = models.CharField(max_length=200)

	class Meta:
		verbose_name = _('Add Project')
		verbose_name_plural = _('Add Projects')

	def __unicode__(self):
		return self.project_name
    

class ProjectProgress(models.Model):
	project_name = models.ForeignKey(Project)
	progress_name = models.CharField(max_length=200)
	progress_details = models.TextField()


	class Meta:
		verbose_name = _('Project Progress')
		verbose_name_plural = _('Project Progress')

	def __unicode__(self):
		return self.progress_name
    