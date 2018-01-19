import pygraphviz as pgv
import time
import os
#from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest,HttpRequest
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import resolve
from django.contrib.auth.decorators import login_required,user_passes_test
from ..models import Host,Service



def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        #print 'non trovato nel DB'
        return None

#def index(request):
#    host_list = Host.objects.all()
#    context = {'host_list': host_list}
#    return render(request, 'avvocatura/index.html', context)

@login_required
def spegnimento_doc(request):
    return render(request, 'avvocatura/spegnere.html')

@login_required
def accensione_doc(request):
    return render(request, 'avvocatura/accendere.html')

@login_required()
def serve_secure_static(request, file_root=os.path.join(settings.STATIC_ROOT, 'nginx-docs')):
    #if not request.method == 'GET':
    #    return HttpResponseBadRequest('Only GET allowed')
    #
    #if not 'file' in request.GET:
    #    return HttpResponseBadRequest('File query must be provided')

    # make sire loggen user is allowed to see the file
    # maybe check some custom permission
    current_url = request.path
    print current_url
    path_list=current_url.split("/")
    file_path = path_list[2]
    print file_path
    #file_path = request.GET['file']
    #file_path = "docs/accendere.html"
    

    # if in DEBUG, make Django serve static file
    # because nginx might not be configured
    if settings.DEBUG:
        abs_file_path = os.path.join(file_root, file_path)
        print abs_file_path
        file_data = open(abs_file_path, 'rb').read()
        return HttpResponse(file_data)

    # else make nginx serve static file
    else:
        redirect_url = '/static-docs/%s' % file_path
        response = HttpResponse()
        response['X-Accel-Redirect'] = redirect_url
        return response


