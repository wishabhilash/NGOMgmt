from django import template

register = template.Library()

# def tableWidth(value):
# 	max_value = 0
# 	for fieldset in value:
		
@register.inclusion_tag("download_button.html")
def download_url(value, value2, url):
	import os
	filter_value = value.split('/')[-1]
	dirname = ""
	if '?' not in filter_value:
		dirname = value
		filter_value = ""
	else:
		dirname = os.path.dirname(value)
	return {
		'download_url' : os.path.join(dirname, url,filter_value),
		'button_value' : value2,
	}

