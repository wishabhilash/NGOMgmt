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


@register.inclusion_tag('preview_submit_line.html', takes_context=True)
def preview_submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    edit = context['edit_enable']
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    ctx = {
        'opts': opts,
        'onclick_attrib': (opts.get_ordered_objects() and change
                            and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and change and context.get('show_delete', True)),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and
                            not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True,
        'show_edit' : edit,
        'download' : context['payslip_download_enable'],
    }
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx
