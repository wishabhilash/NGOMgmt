from os import path
from south.db import db
from django.db import models
import dynamic
from .models import PayslipHead

COLUMN_PREFIX = 'payslip_'
TABLE_NAME = 'hrms_employeepayslip'


def write_file(heads):
	dynamic_models_path = path.join(path.dirname(__file__),'dynamic_models.py')
	fields = """"""
	for head in heads:
		fields += "\t" + COLUMN_PREFIX + "%s = %s\n" % (head.head_name.lower(),dynamic.IntegerField())

	f = open(dynamic_models_path,'w')
	f.write((dynamic.imports + dynamic.model_header + dynamic.model_attrs + fields + dynamic.model_footer) % 
	('EmployeePayslip','EmployeePayslip','EmployeePayslip'))
	f.close()



def pre_delete_payslip_signal(sender, **kwargs):
	global LAST_DEL_SCHEMA
	global NO_REPEAT
	NO_REPEAT = False
	LAST_DEL_SCHEMA = set([head.head_name for head in sender.objects.all()])
	print "In pre save"
	print LAST_DEL_SCHEMA

count = 0
def post_delete_payslip_signal(sender, **kwargs):
	global LAST_DEL_SCHEMA
	global NO_REPEAT
	global count
	if not NO_REPEAT:
		count += 1
		print count
		NO_REPEAT = True
		print "In post save: LAST_SCHEMA"
		print LAST_DEL_SCHEMA
		heads = sender.objects.all()
		CURRENT_SCHEMA = set([head.head_name for head in heads])
		# print "In post save: CURRENT_SCHEMA"
		del_cols = list(LAST_DEL_SCHEMA - CURRENT_SCHEMA)
		print del_cols
		
		db_altered = False
		for del_col in del_cols:
			# pass
			# print del_col
			db.delete_column(TABLE_NAME,COLUMN_PREFIX + del_col)
		db_altered = True

		if db_altered:
			write_file(heads)
	

def pre_save_payslip_signal(sender, **kwargs):
	global LAST_ADD_SCHEMA
	LAST_ADD_SCHEMA = set([head.head_name for head in sender.objects.all()])
	#print "In pre save"
	#print LAST_ADD_SCHEMA



def post_save_payslip_signal(sender, **kwargs):
	global LAST_ADD_SCHEMA
	#print "In post save: LAST_ADD_SCHEMA"
	print LAST_ADD_SCHEMA
	heads = sender.objects.all()
	CURRENT_SCHEMA = set([head.head_name for head in heads])
	#print "In post save: CURRENT_SCHEMA"
	print CURRENT_SCHEMA
	print CURRENT_SCHEMA
	add_col = list(CURRENT_SCHEMA - LAST_ADD_SCHEMA)
	print add_col

	db_updated = False
	from south.db import db
	db.add_column(TABLE_NAME,COLUMN_PREFIX + add_col[0],models.IntegerField(null=True))
	db_updated = True

	if db_updated:
		write_file(heads)



def post_save_employee_signal(sender, **kwargs):
	# print sender.
	pass