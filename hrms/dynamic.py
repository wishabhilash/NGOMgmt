# from django.db import models
# from django.utils.translation import ugettext_lazy as _

def IntegerField():
	return "models.IntegerField(null=True)"

def CharField(max_length=200):
	return "models.CharField(max_length=" + str(max_length) + ", blank=True)"

imports = """from django.db import models
from django.utils.translation import ugettext_lazy as _
from models import *\n\n"""

model_header = """class %s(models.Model):\n"""
model_footer = """\tclass Meta:
		verbose_name = _('%s')
		verbose_name_plural = _('%ss')

	def __unicode__(self):
		return self.employee_name

"""

model_attrs = """	employee_name = models.ForeignKey(Employee)
	# issue_date = models.DateField(auto_now_add=True)
	
"""



# print (model_header + model_attrs + model_footer) % ("asfa","asda","asda")