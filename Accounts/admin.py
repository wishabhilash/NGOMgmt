from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *
from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response


class PayFundAdmin(admin.ModelAdmin):
	"""docstring for PayFundAdmin"""
	
	def save_model(self, request, obj, form, change):
		super(PayFundAdmin, self).save_model(request, obj, form, change)
		print type(obj.head_name)
		print type(obj.paid_to)



admin.site.register(IncomeHead)
admin.site.register(PaymentHead)
admin.site.register(RecieveFund)
admin.site.register(PayFund, PayFundAdmin)