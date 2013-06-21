from django.db import models
from django.utils.translation import ugettext_lazy as _
from models import *

class EmployeePayslip(models.Model):
	employee_name = models.ForeignKey(Employee)
	
	payslip_ta = models.IntegerField(null=True)
	payslip_la = models.IntegerField(null=True)
	payslip_da = models.IntegerField(null=True)
	payslip_ma = models.IntegerField(null=True)
	class Meta:
		verbose_name = _('EmployeePayslip')
		verbose_name_plural = _('EmployeePayslips')

	def __unicode__(self):
		return "%s %s" % (self.employee_name.first_name,self.employee_name.last_name)

