from django.conf.urls import url

from views import graphviz_views,manage_views,auth_views,docs_views

urlpatterns = [
    url(r'^$', graphviz_views.index, name='index'),
    url(r'^login/$', auth_views.user_login, name='login'),
    url(r'^logout/$', auth_views.user_logout, name='logout'),
    url(r'^hosts/$', graphviz_views.hosts_index, name='hosts_index'),
    url(r'^servizi/$', graphviz_views.servizi_index, name='servizi_index'),
    url(r'^hosts/graph/(?P<id>[a-zA-Z0-9_]+)/$', graphviz_views.host_detail, name='host_detail'),
    url(r'^servizi/graph/(?P<id>[a-zA-Z0-9_]+)/$', graphviz_views.service_detail, name='service_detail'),
    #url(r'^gestione/$', manage_views.manage_index, name='manage_index'),
    url(r'^hosts/add/$', manage_views.host_add, name='host_add'),
    url(r'^servizi/add/$', manage_views.service_add, name='service_add'),
    url(r'^hosts/update/(?P<id>[a-zA-Z0-9_]+)/$', manage_views.host_update, name='host_update'),
    url(r'^servizi/update/(?P<id>[a-zA-Z0-9_]+)/$', manage_views.service_update, name='service_update'),
    url(r'^hosts/delete/(?P<id>[a-zA-Z0-9_]+)/$', manage_views.host_delete, name='host_delete'),
    url(r'^servizi/delete/(?P<id>[a-zA-Z0-9_]+)/$', manage_views.service_delete, name='service_delete'),
    #url(r'^docs/spegnimento/', docs_views.spegnimento_doc, name='spegnimento_doc'),
    #url(r'^docs/accensione/', docs_views.accensione_doc, name='accensione_doc'),
    url(r'^docs/', docs_views.serve_secure_static, name='serve_secure_static')


    #url(r'^hosts/$', views.service_detail, name='service_detail'),

]