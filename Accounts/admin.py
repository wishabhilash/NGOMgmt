from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *
from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response


admin.site.register(IncomeHead)
admin.site.register(PaymentHead)
admin.site.register(RecieveFund)
admin.site.register(PayFund)