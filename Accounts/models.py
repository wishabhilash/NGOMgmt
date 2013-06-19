from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class IncomeHead(models.Model):
	head_name = models.CharField(max_length=200)

	class Meta:
		verbose_name = _('Income Head')
		verbose_name_plural = _('Income Heads')

	def __unicode__(self):
		return self.head_namee
    

class PaymentHead(models.Model):
	payment_name = models.CharField(max_length=200)

	class Meta:
		verbose_name = _('Payment Head')
		verbose_name_plural = _('Payment Heads')

	def __unicode__(self):
		return self.payment_name
    

class RecieveFund(models.Model):
	date = models.DateField()
	rcvid = models.CharField(max_length=100)
	head_name = models.ForeignKey(IncomeHead)
	recieved_from = models.CharField(max_length=200)
	particulars = models.TextField()
	amount = models.IntegerField()
	in_words = models.TextField()

	class Meta:
		verbose_name = _('Recieve Fund')
		verbose_name_plural = _('Recieve Funds')

	def __unicode__(self):
		return self.recieved_from


class PayFund(models.Model):
	date = models.DateField()
	rcvid = models.CharField(max_length=100)
	head_name = models.ForeignKey(PaymentHead)
	paid_to = models.CharField(max_length=200)
	particulars = models.TextField()
	amount = models.IntegerField()
	in_words = models.TextField()
	
	class Meta:
		verbose_name = _('Pay Fund')
		verbose_name_plural = _('Pay Funds')

	def __unicode__(self):
		return self.paid_to
    