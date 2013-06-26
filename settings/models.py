from django.db import models

# Create your models here.

class OrganisationDetails(models.Model):
	org_name = models.CharField(max_length=200)
	org_address = models.TextField()
	ph_num = models.CharField(max_length=20)
	fax_num = models.CharField(max_length=20)
	mail_id = models.EmailField()

    class Meta:
        verbose_name = _('Organisation Details')
        verbose_name_plural = _('Organisation Detailss')

    def __unicode__(self):
        pass
    
