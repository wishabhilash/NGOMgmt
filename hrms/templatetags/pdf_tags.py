from django import template

register = template.Library()


@register.inclusion_tag("pdf_header.html")
def pdf_headers(value):
	return {'headers' : value}

@register.inclusion_tag("pdf_table_data.html")
def pdf_data(value):
	return {'data_list' : value}