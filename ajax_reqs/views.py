# Create your views here.
from django.shortcuts import (render_to_response, HttpResponse)
from hrms.models import Employee
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import simplejson



@login_required
def employee_ajax(request):
	query_data = request.REQUEST['filter']
	query_num = request.REQUEST['pagesize']
	data = Employee.objects.filter(Q(first_name__startswith = query_data) | Q(last_name__startswith = query_data))[:int(query_num)]
	jsonp = request.REQUEST['jsonp']
	to_json = {
		'users' : [{'display_name' :user.first_name} for user in data],
	}
	print jsonp + "(" + simplejson.dumps(to_json) + ")"
	return HttpResponse(jsonp + "(" + simplejson.dumps(to_json) + ")", mimetype="application/json")