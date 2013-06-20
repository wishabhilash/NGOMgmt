# Create your views here.
from django.shortcuts import (render_to_response, HttpResponse)
from hrms.models import Employee
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import simplejson
from django.db.models.query import QuerySet



@login_required
def employee_ajax(request):
	query_data = request.REQUEST['filter']
	query_num = request.REQUEST['pagesize']
	query_words = query_data.split()
	data = []
	for query in query_words:
		data += list(Employee.objects.filter(Q(emp_id__istartswith = query) | Q(first_name__istartswith = query) | Q(last_name__istartswith = query))[:int(query_num)])
	jsonp = request.REQUEST['jsonp']
	to_json = {
		'users' : [{'display_name' :user.first_name} for user in data],
	}
	print jsonp + "(" + simplejson.dumps(to_json) + ")"
	return HttpResponse(jsonp + "(" + simplejson.dumps(to_json) + ")", mimetype="application/json")
