# from django.db import models
# from django.utils.translation import ugettext_lazy as _

def IntegerField():
	return "models.IntegerField(null=True)"

def CharField(max_length=200):
	return "models.CharField(max_length=" + str(max_length) + ", blank=True)"

imports = """from django.db import models
from django.utils.translation import ugettext_lazy as _
from models_static import *\n\n"""

model_header = """class %s(models.Model):\n"""
model_footer = """\tclass Meta:
		verbose_name = _('%s')
		verbose_name_plural = _('%ss')

	def __unicode__(self):
		return ""

"""

model_attrs = """	employee_name = models.ForeignKey(Employee)
	
"""



# print (model_header + model_attrs + model_footer) % ("asfa","asda","asda")