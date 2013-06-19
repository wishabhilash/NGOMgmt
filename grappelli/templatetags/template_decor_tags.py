from django import template

register = template.Library()


@register.filter(name = 'purify_name')
def purify_name(value):
	dic = {
		'Auth' : 'Authentication',
		'Accounts' : 'Accounts',
		'Hrms' : 'Human Resource Management',
		'Project' : 'Project Details',
		'Sites' : 'Site Management',
	}

	return dic[value]

@register.filter(name = 'row_mod')
def row_mod(value):
	return value%3

@register.filter
def icon_name(value):
	dic = {
		'Auth' : 'auth.png',
		'Accounts' : 'accounts.png',
		'Hrms' : 'hrms.png',
		'Project' : 'projects.png',
		'Sites' : 'auth.png',	
	}
	return dic[value]