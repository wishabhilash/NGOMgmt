from django import template

register = template.Library()

# def tableWidth(value):
# 	max_value = 0
# 	for fieldset in value:
		
@register.filter(name='download_url')
def download_url(value):
	# import os
	# filter_value = value.split('/')[-1]
	# dirname = ""
	# if '?' not in filter_value:
	# 	dirname = value
	# else:
	# 	dirname = os.path.dirname(value)
	# return os.path.join(dirname, 'download',filter_value)
	return "download"
