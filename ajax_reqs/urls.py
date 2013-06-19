from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:


urlpatterns = patterns('',
    url(r'^autocomplete/$', 'ajax_reqs.views.employee_ajax'),
)


