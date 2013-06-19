from django.db import models
from django.utils.translation import ugettext_lazy as _
from NGOMgt import settings
# from dynamic_models import *

# Create your models here.

# class EmployeeJobHistory(models.Model):
# 	# JOB DETAILS
# 	job_title = models.CharField(max_length=100)
# 	experience_info = models.CharField(max_length=200)
# 	experience_start = models.DateField(auto_now_add=True)
# 	experience_end = models.DateField(auto_now_add=True)

# 	class Meta:
# 		verbose_name = _('Employee Career')
# 		verbose_name_plural = _('Employee Career')
# 		# app_label = "HRMSs"
    
# 		def __unicode__(self):
# 			pass
            


class Employee(models.Model):
	emp_id = models.CharField(max_length=50,blank=True)

	#PERSONAL DETAILS
	first_name = models.CharField(max_length=200)
	middle_name = models.CharField(max_length=100, blank=True)
	last_name = models.CharField(max_length=100)
	gender = models.CharField(max_length=1)
	dob = models.DateField()
	marital_status = models.CharField(max_length=20)
	father_name = models.CharField(max_length=200, blank=True)
	mother_name = models.CharField(max_length=200, blank=True)
	blood_group = models.CharField(max_length=5, blank=True)
	nationality = models.CharField(max_length=30)
	photo = models.ImageField(upload_to=settings.MEDIA_URL, blank=True)

	# JOB DETAILS
	designation = models.CharField(max_length=100, blank=True)
	join_date = models.DateField()
	qualification = models.CharField(max_length=100, blank=True)
	# job_list = models.ForeignKey(EmployeeJobHistory, blank=True)

	
	# CONTACT DETAILS
	email = models.EmailField(max_length=200, blank=True)
	home_address = models.TextField(max_length=400, blank=True)
	phone_no = models.CharField(max_length=20,help_text='Enter your mobile number', blank=True)
	
	# ACCOUNT DETAILS
	bank_name = models.CharField(max_length=200, blank=True)
	branch = models.CharField(max_length=200, blank=True)
	account_no = models.CharField(max_length=25, blank=True)
	ifsc_no = models.CharField(max_length=25, blank=True)

	# IDENTIFICATION DETAILS
	passport_no = models.CharField(max_length=25, blank=True)
	pan_no = models.CharField(max_length=25, blank=True)
	dl_no = models.CharField(max_length=25, blank=True)
	id_card_no = models.CharField(max_length=25, blank=True)


	class Meta:
		verbose_name = _('Employee Details')
		verbose_name_plural = _('Employees Details')

	def __unicode__(self):
		return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

	

class PayslipHead(models.Model):
	head_name = models.CharField(max_length=50)
	head_type = models.CharField(max_length=100)
	
	class Meta:
		verbose_name = _('Payslip Head')
		verbose_name_plural = _('Payslip Heads')

	def __unicode__(self):
		return "%s" % self.head_name



# def create_dynamic_employee_payslip():
# 	class Meta:
# 		verbose_name = _('EmployeePayslip')
# 		verbose_name_plural = _('EmployeePayslips')
# 		app_label = _('HRMS')

# 	def get_dynamic_attrs():
# 		return { 'payslip_' + head.head_name.lower() : models.IntegerField() for head in PayslipHead.objects.all()}
# 		# dic = {}
# 		# heads = PayslipHead.objects.all()
# 		# for head in heads:
# 		# 	dic['payslip_' + head.head_name.lower()] = models.IntegerField()
# 		# return dic


# 	def __unicode__(self):
# 		return self.employee__first_name + self.employee__middle_name + self.employee__last_name

# 	attrs = {
# 		'employee' : models.ForeignKey(Employee),
# 		'__module__' : 'HRMS',
# 		'Meta' : Meta,
# 		'__unicode__' : __unicode__,

# 	}
# 	attrs.update(get_dynamic_attrs())

# 	return type('EmployeePayslip', (models.Model,), attrs)



# EmployeePayslip = create_dynamic_employee_payslip()




# SIGNALS
# from .signals import *

# models.signals.post_delete.connect(post_delete_payslip_signal, PayslipHead, dispatch_uid = "post_delete_id_1")
# models.signals.pre_delete.connect(pre_delete_payslip_signal, PayslipHead, dispatch_uid = "pre_delete_id_1")
# models.signals.post_save.connect(post_save_payslip_signal, PayslipHead, dispatch_uid = "post_save_id_1")
# models.signals.pre_save.connect(pre_save_payslip_signal, PayslipHead, dispatch_uid = "pre_save_id_1")