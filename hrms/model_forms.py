from django import forms
from models import *
from django.utils.translation import ugettext_lazy as _

class EmployeeForm(forms.ModelForm):
	gender = forms.ChoiceField(choices=(('m','Male'),('f','Female')))
	marital_status = forms.ChoiceField(choices=(('single','Single'),('married','Married')))
	
	labels = {
		'dob' : 'Date of Birth',
	}
	
	def clean_join_date(self):
		if self.cleaned_data['join_date'] <= self.cleaned_data['dob']:
			raise forms.ValidationError("You can't join before your birth :P")
		return self.cleaned_data['join_date']

	def clean_email(self):
		if self.instance.id:
			instance_data = Employee.objects.get(pk=self.instance.id)
			data = None
			try:
				data = Employee.objects.get(email = self.cleaned_data['email'])
			except:
				pass
			if not data:
				return self.cleaned_data['email']
			else:
				if instance_data.id != data.id:
					raise forms.ValidationError("Email already exists")
				else:
					return self.cleaned_data['email']
		else:
			try:
				data = Employee.objects.get(email = self.cleaned_data['email'])
			except:
				return self.cleaned_data['email']
			raise forms.ValidationError("Email already exists")
		
	class Meta:
		model = Employee




    

def get_payslip_head_form():
	class Meta:
		model = PayslipHead
	
	HEAD_TYPE_CHOICES = (
		('income',"Income"),
		('deduction',"Deduction"),
	)


	attrs = {
		'head_name': forms.CharField(max_length=200, label='Head Name'),
		'head_type' : forms.ChoiceField(choices = HEAD_TYPE_CHOICES, label='Head Type'),
		'Meta' : Meta,
	}

	return type('PayslipHeadForm',(forms.ModelForm,), attrs)



class CustomTextInput(forms.TextInput):
	"""docstring for CustomTextInput"""
	class Media:
		js = (
			'/static/hrms/js/autocomplete.js',
		)

		css = {
			'all' : ('/static/hrms/css/hrms_style.css',)
		}


def get_employee_payslip_form():
	class Meta:
		model = EmployeePayslip

	def get_attrs():
		heads = PayslipHead.objects.all()
		return {'payslip_'+head.head_name.lower() : forms.IntegerField(label=head.head_name.upper()) for head in heads}

	attrs = {
		'employee_name' : forms.CharField(max_length=50,
			widget = CustomTextInput({
				'id' : 'ajax-search-field',
				})),
		'gross_income' : forms.CharField(max_length=50),
		'net_income' : forms.CharField(max_length=50),

	}

	attrs.update(get_attrs())

	return type('EmployeePayslipForm', (forms.ModelForm,), attrs)