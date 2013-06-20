from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *
from django.shortcuts import render_to_response
from functools import update_wrapper
from django.template import RequestContext
from django.http import HttpResponse
from .models import *
from .model_forms import *


class EmployeeAdmin(admin.ModelAdmin):
	"""docstring for Employee"""
	list_filter = ('first_name', 'last_name',)
	search_fields = ('^first_name', '^last_name')
	list_display = ('full_name', 'email', 'phone_no')
	exclude = ['emp_id',]
	form = EmployeeForm
	fieldsets = (
			('Personal Details',{
					'fields':(
						('first_name','middle_name'),
						('last_name','dob'),
						('gender','marital_status'),
						('father_name','mother_name'),
						('blood_group','nationality'),
						('photo'),
						),
				}),
			('Job Details',{
					'fields':(
						('designation','qualification'),
						('join_date'),
						),
				}),
			('Contact Details',{
					'fields':(
						('phone_no','email'),
						'home_address',
						),
				}),
			('Account Details',{
					'fields':(
						('bank_name', 'branch'),
						('account_no','ifsc_no'),
						),
				}),
			('Identification Details',{
					'fields':(
						('passport_no','pan_no'),
						('dl_no','id_card_no'),
						),
				}),
		)

	def full_name(self, obj):
		return obj.first_name + " " + obj.last_name

	full_name.short_description = "Name"

	def save_model(self, request, obj, form, change):
		super(EmployeeAdmin, self).save_model(request, obj, form, change)
		obj.emp_id = "EMP" + str(obj.id)
		obj.save()



	def get_urls(self):
		from django.conf.urls.defaults import patterns, url
		def wrap(view):
			def wrapper(*args, **kwargs):
				return self.admin_site.admin_view(view)(*args, **kwargs)
			return update_wrapper(wrapper, view)

		info = self.model._meta.app_label, self.model._meta.module_name

		urls = super(EmployeeAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^download/$',
				wrap(self.employee_view),
				name='%s_%s_new' % info),
		)
		# print my_urls + urls
		return my_urls + urls

	def employee_view(self,request, extra_context = None):
		res = self.changelist_view(request, extra_context = extra_context)
		res.template_name = 'mytemplate.html'

		return res



admin.site.register(Employee, EmployeeAdmin)



class PayslipHeadAdmin(admin.ModelAdmin):
	"""docstring for PayslipHeadAdmin"""
	list_display = ('head_name','head_type')	
	form = get_payslip_head_form()
		

admin.site.register(PayslipHead, PayslipHeadAdmin)



def get_employee_payslip_fieldsets():
	data = PayslipHead.objects.all()
	retData = []
	income_fieldset = ('Income',{
		'fields':'',
		})

	deduction_fieldset = ('Deduction',{
		'fields':'',
		})

	income_fields = []
	deduction_fields = []
	income_row = []
	deduction_row = []

	for dat in data:
		if dat.head_type.lower() == 'income':
			income_row.append('payslip_' + dat.head_name.lower())
		else:
			deduction_row.append('payslip_' + dat.head_name.lower())


	def realign_text_boxes(lis):
		ret_list = []
		count = 0
		temp_list = []
		for i in lis:
			temp_list.append(i)
			count += 1
			if count == 2:
				ret_list.append(tuple(temp_list))
				temp_list = []
				count = 0
		if temp_list: ret_list.append(tuple(temp_list))
		return tuple(ret_list)

		
	if income_row:
		income_fields = realign_text_boxes(income_row)
	if deduction_row:
		deduction_fields = realign_text_boxes(deduction_row)


	income_fieldset[1]['fields'] = tuple(income_fields)
	deduction_fieldset[1]['fields'] = tuple(deduction_fields)

	# print [income_fieldset, deduction_fieldset]
	return [income_fieldset, deduction_fieldset]


class EmployeePayslipAdmin(admin.ModelAdmin):
	"""docstring for PayslipAdmin"""
	
	form = get_employee_payslip_form()
	fieldsets = tuple([
		("Details", {
			'fields' : ('employee_name',),
		},)
	] + get_employee_payslip_fieldsets()
	+ [('Finance Details',{
			'fields' : (
				('gross_income', 'net_income'),
				),
		})]
	)


	

	def get_urls(self):
		from django.conf.urls.defaults import patterns, url
		def wrap(view):
			def wrapper(*args, **kwargs):
				return self.admin_site.admin_view(view)(*args, **kwargs)
			return update_wrapper(wrapper, view)

		info = self.model._meta.app_label, self.model._meta.module_name

		urls = super(EmployeePayslipAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^download/$',
				wrap(self.employee_view),
				name='%s_%s_new' % info),
		)
		# print my_urls + urls
		return my_urls + urls

	def employee_view(self,request, extra_context = None):
		res = self.changelist_view(request, extra_context = extra_context)
		res.template_name = 'mytemplate.html'

		return res


admin.site.register(EmployeePayslip, EmployeePayslipAdmin)