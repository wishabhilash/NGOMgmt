from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *
from django.shortcuts import render_to_response
from functools import update_wrapper
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .model_forms import *
from reportlab.pdfgen import canvas
import xlwt
from django.contrib.admin.templatetags import admin_list
import re
from django.core.urlresolvers import reverse
from django.template import loader
import weasyprint
		

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
						('photo', 'pf_id'),
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
		print info
		urls = super(EmployeeAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^(\d*)/$',
                wrap(self.form_preview),
                name='%s_%s_preview' % info),
			url(r'^(\d*)/edit/$',
                wrap(self.change_view),
                name='%s_%s_change' % info),
			url(r'^(\d*)/download/$',
                wrap(self.download_details_view),
                name='%s_%s_download_details' % info),
			url(r'^download/$',
				wrap(self.download_view),
				name='%s_%s_download' % info),
			url(r'^download/pdf/$',
				wrap(self.download_as_pdf_view),
				name='%s_%s_download_as_pdf' % info),
			url(r'^download/excel/$',
				wrap(self.download_as_excel_view),
				name='%s_%s_download_as_excel' % info),
		)
		# print my_urls + urls
		return my_urls + urls

	def response_post_save_change(self, request, obj):
		"""
		Figure out where to redirect after the 'Save' button has been pressed
		when editing an existing object.
		"""
		print obj.id
		opts = self.model._meta
		if self.has_change_permission(request, None):
			post_url = reverse('admin:%s_%s_preview' %
								(opts.app_label, opts.module_name),
								current_app=self.admin_site.name, args=[obj.id])
		else:
			post_url = reverse('admin:index',
								current_app=self.admin_site.name)
		return HttpResponseRedirect(post_url)


	def download_details_view(self,request, object_id,extra_context = None):
		# return self.
		# obj = self.get_object(request, object_id)

		# emp_obj = Employee.objects.get(pk=obj.employee_name_id)
		# print emp_obj.first_name
		# context = {
		# 	'company_name' : "Jyodiv",
		# 	'company_address' : '''andan\nakjnsda\naksna''',
		# 	'employee_designation' : str(emp_obj.designation).lower().capitalize(),
		# 	'employee_name' : str(obj.employee_name).lower().capitalize(),

		# }

		# html = loader.render_to_string("payslip.html", context)
		# response = HttpResponse(mimetype="application/pdf")
		# response['Content-Disposition'] = 'attachment; filename="payslip.pdf"'
		# weasyprint.HTML(string=html).write_pdf(response)
		# return response
		raise NotImplementedError("Not Implemented Yet!!!")


	def change_view(self,request, object_id,extra_context = None):
		res = super(EmployeeAdmin, self).change_view(request, object_id,extra_context = None)
		res.template_name = 'modified_change_form.html'
		return res


	def form_preview(self,request, object_id,extra_context = None):
		res = self.change_view(request, object_id, extra_context = None)
		res.template_name = 'change_form_preview.html'
		res.context_data['edit_enable'] = True
		res.context_data['payslip_download_enable'] = True
		return res


	def download_view(self,request, extra_context = None):
		res = self.changelist_view(request, extra_context = extra_context)
		res.template_name = 'mytemplate.html'
		res.context_data['pdf_enable'] = True
		res.context_data['excel_enable'] = True
		return res


	def download_as_pdf_view(self,request, extra_context = None):
		from weasyprint import CSS, HTML

		css_string = """@page {
							size: A4;
							margin : 1.5cm;
						}
						"""


		template_response = self.changelist_view(request, extra_context = extra_context)
		cl = template_response.context_data['cl']
		response = HttpResponse(content_type = 'application/pdf')
		response['Content-Disposition'] = 'attachment; filename="pdfreport.pdf"'

		table_data = self.get_table_data(cl)
		context = {
			'headers' : table_data['headers'],
			'data' : table_data['data']
		}
		html = loader.render_to_string("list_print.html", context)
		print html
		weasyprint.HTML(string=html).write_pdf(response)
		return response


	
	def download_as_excel_view(self,request, extra_context = None):
		res = self.changelist_view(request, extra_context = extra_context)

		book = xlwt.Workbook(encoding='utf8')
		sheet = book.add_sheet("untitled")

		default_style = xlwt.Style.default_style
		datetime_style = xlwt.easyxf(num_format_str = 'dd/mm/yyyy hh:mm')
		date_style = xlwt.easyxf(num_format_str = 'dd/mm/yyyy')

		response = HttpResponse(content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename="xlreport.xls"'
		book.save(response)
		return response

	def get_table_data(self, cl):
		ret_dict = {}
		ret_list = []
		headers = [header['text'] for header in admin_list.result_headers(cl)]
		headers.pop(0)
		ret_dict['headers'] = headers
		patt = r'<th .+><a .+>(.*)</a></th>|<td>(.*)</td>'

		for result in admin_list.results(cl):
			temp_list = []
			for item in result:
				res = re.findall(patt, item)
				if res:
					# temp_list.append( "" if (res[0][0] or res[0][1]) == "&nbsp;" else res[0][0] or res[0][1])
					temp_list.append(res[0][0] or res[0][1])
			ret_list.append(temp_list)
		ret_dict['data'] = ret_list
		return ret_dict


admin.site.register(Employee, EmployeeAdmin)






class PayslipHeadAdmin(admin.ModelAdmin):
	"""docstring for PayslipHeadAdmin"""
	list_display = ('head_name','head_type')
	form = get_payslip_head_form()
	actions = ['change_to_income']

	
	def change_to_income(self, request, queryset):
		queryset.update(head_type = 'deduction')
	change_to_income.short_description = "Mark selected as income"
	

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
	
	search_fields = ['employee_name__emp_id','employee_name__first_name','employee_name__last_name']	
	form = get_employee_payslip_form()
	list_display = [field.name for field in EmployeePayslip._meta.fields if field.name.lower() != "id"] + ['net_income', 'gross_income']
	actions = ('download_selected_as_pdf',)
	fieldsets = tuple([
		("Details", {
			'fields' : ('employee_name_mask','employee_name'),
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
		print info
		urls = super(EmployeePayslipAdmin, self).get_urls()
		my_urls = patterns('',
			url(r'^(\d*)/$',
                wrap(self.form_preview),
                name='%s_%s_preview' % info),
			url(r'^(\d*)/edit/$',
                wrap(self.change_view),
                name='%s_%s_change' % info),
			url(r'^(\d*)/download/$',
                wrap(self.download_details_view),
                name='%s_%s_download_details' % info),
			url(r'^download/$',
				wrap(self.download_view),
				name='%s_%s_download' % info),
			url(r'^download/pdf/$',
				wrap(self.download_as_pdf_view),
				name='%s_%s_download_as_pdf' % info),
			url(r'^download/excel/$',
				wrap(self.download_as_excel_view),
				name='%s_%s_download_as_excel' % info),
		)
		# print my_urls + urls
		return my_urls + urls

	def response_post_save_change(self, request, obj):
		"""
		Figure out where to redirect after the 'Save' button has been pressed
		when editing an existing object.
		"""
		print obj.id
		opts = self.model._meta
		if self.has_change_permission(request, None):
			post_url = reverse('admin:%s_%s_preview' %
								(opts.app_label, opts.module_name),
								current_app=self.admin_site.name, args=[obj.id])
		else:
			post_url = reverse('admin:index',
								current_app=self.admin_site.name)
		return HttpResponseRedirect(post_url)

	def download_details_view(self,request, object_id,extra_context = None):
		obj = self.get_object(request, object_id)

		emp_obj = Employee.objects.get(pk=obj.employee_name_id)
		print emp_obj.first_name
		context = {
			'company_name' : "Jyodiv",
			'company_address' : '''andan\nakjnsda\naksna''',
			'employee_designation' : str(emp_obj.designation).lower().capitalize(),
			'employee_name' : str(obj.employee_name).lower().capitalize(),

		}

		html = loader.render_to_string("payslip.html", context)
		response = HttpResponse(mimetype="application/pdf")
		response['Content-Disposition'] = 'attachment; filename="payslip.pdf"'
		weasyprint.HTML(string=html).write_pdf(response)
		return response



	def change_view(self,request, object_id,extra_context = None):
		res = super(EmployeePayslipAdmin, self).change_view(request, object_id,extra_context = None)
		res.template_name = 'modified_change_form.html'
		return res


	def form_preview(self,request, object_id,extra_context = None):
		res = self.change_view(request, object_id, extra_context = None)
		res.template_name = 'change_form_preview.html'
		res.context_data['edit_enable'] = True
		res.context_data['payslip_download_enable'] = True
		return res


	def download_view(self,request, extra_context = None):
		res = self.changelist_view(request, extra_context = extra_context)
		res.template_name = 'mytemplate.html'
		res.context_data['pdf_enable'] = True
		res.context_data['excel_enable'] = True
		return res


	def download_as_pdf_view(self,request, extra_context = None):
		from weasyprint import CSS, HTML

		css_string = """@page {
							size: A4;
							margin : 1.5cm;
						}
						"""


		template_response = self.changelist_view(request, extra_context = extra_context)
		cl = template_response.context_data['cl']
		response = HttpResponse(content_type = 'application/pdf')
		response['Content-Disposition'] = 'attachment; filename="pdfreport.pdf"'

		table_data = self.get_table_data(cl)
		context = {
			'headers' : table_data['headers'],
			'data' : table_data['data']
		}
		html = loader.render_to_string("list_print.html", context)
		print html
		weasyprint.HTML(string=html).write_pdf(response)
		return response


	
	def download_as_excel_view(self,request, extra_context = None):
		res = self.changelist_view(request, extra_context = extra_context)

		book = xlwt.Workbook(encoding='utf8')
		sheet = book.add_sheet("untitled")

		default_style = xlwt.Style.default_style
		datetime_style = xlwt.easyxf(num_format_str = 'dd/mm/yyyy hh:mm')
		date_style = xlwt.easyxf(num_format_str = 'dd/mm/yyyy')

		response = HttpResponse(content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename="xlreport.xls"'
		book.save(response)
		return response

	def get_table_data(self, cl):
		ret_dict = {}
		ret_list = []
		headers = [header['text'] for header in admin_list.result_headers(cl)]
		headers.pop(0)
		ret_dict['headers'] = headers
		patt = r'<th .+><a .+>(.*)</a></th>|<td>(.*)</td>'

		for result in admin_list.results(cl):
			temp_list = []
			for item in result:
				res = re.findall(patt, item)
				if res:
					# temp_list.append( "" if (res[0][0] or res[0][1]) == "&nbsp;" else res[0][0] or res[0][1])
					temp_list.append(res[0][0] or res[0][1])
			ret_list.append(temp_list)
		ret_dict['data'] = ret_list
		return ret_dict

	def net_income():
		return ""

	def gross_income():
		return ""


admin.site.register(EmployeePayslip, EmployeePayslipAdmin)
