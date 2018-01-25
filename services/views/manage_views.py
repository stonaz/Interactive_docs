import pygraphviz as pgv
#from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from ..models import Host,Service
from utils import *
from django.contrib.auth.decorators import login_required,user_passes_test

tipi_servizio = ['Batch','Middleware','Applicativo']
tipi_documentazione = ['Testo','Link','Codice']

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_index(request):
    context = {}
    #services_list = Service.objects.all()
    #host_list = Host.objects.all()
    return render(request, 'services/manage_index.html', context) 


@login_required
@user_passes_test(lambda u: u.is_superuser,login_url='/login/')
def service_add(request):
    message=""
    host_list = Host.objects.all()
    services_list = Service.objects.all()
    service_to_update_deps_to_before= None
    service_to_update_deps_by_before= None
    menu_id='service_mgt'
    context = {'services_list': services_list,'host_list': host_list,'menu':menu_id,
               'message':message,'tipi_servizio':tipi_servizio, 'tipi_documentazione':tipi_documentazione}
    
    if request.POST:
        user_data = request.POST
        print user_data
        name=request.POST['name']
        port=request.POST['port']
        desc=request.POST['desc']
        documentation_url=request.POST['documentation_url']
        host = request.POST['host']
        service_type = request.POST['service_type']
        deploy_doc_type = request.POST['deploy_doc_type']
        start_doc_type = request.POST['start_doc_type']
        stop_doc_type = request.POST['stop_doc_type']
        svn = request.POST['svn']
        deploy = request.POST['deploy']
        start = request.POST['start']
        stop = request.POST['stop']
        user = request.POST['user']
        password = request.POST['password']
        deps_to = request.POST.getlist('deps_to')
        deps_by = request.POST.getlist('deps_by')
        service=Service(name=name,port=port,host=host,desc=desc,service_type=service_type,
                        deploy_doc_type=deploy_doc_type,start_doc_type=start_doc_type,stop_doc_type=stop_doc_type,
                        svn=svn,user=user,password=password,
                        start=start,stop=stop,documentation_url=documentation_url,deploy=deploy )
        #service.save()
        check_loop_dep = [dep_to for dep_to in deps_to if dep_to in deps_by]
        print len(check_loop_dep)
        if len(check_loop_dep) > 0 :
            print 'esco'
            context["message"]="Errore: aggiunta dipendenza circolare"
            context["user_data"] = user_data
            return render(request, 'services/add_service.html', context)
        else:
            if deps_to:
                print 'Presenti dipendenze_to'
                service.deps_to = deps_to
                dependencies_link_add(service,deps_to,'TO')
                print 'dipendenza to aggunta'
            if deps_by:
                print 'Presenti dipendenze_by'
                service.deps_by = deps_by
                dependencies_link_add(service,deps_to,'BY')
                print 'dipendenza by aggunta'
        
        service.save()
        # Aggiunta del servizio appena creato ai servizi dell'host di appartenenza
        host_to_update = Host.objects.get(name=host)
        host_to_update.services.append(name)
        host_to_update.save()
        context["message"]="Servizio aggiunto"
    return render(request, 'services/add_service.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser,login_url='/login/')
def service_update(request,id):
    message=""
    prev_host = ""
    menu_id='service_mgt'
    services_list = Service.objects.all()
    host_list = Host.objects.all()
    service_deps_by_list=[]
    service_deps_to_list=[]
    
    service_to_update = Service.objects.get(id=id)
    service_to_update_deps_to_before= service_to_update.deps_to
    service_to_update_deps_by_before= service_to_update.deps_by
    #Creazione liste per il template
    for service in services_list:
        service_deps_by = {}
        service_deps_to = {}
        if service.name != service_to_update.name:
            service_deps_by['name'] = service.name        
            service_deps_to['name'] = service.name

            if service and service.name in service_to_update.deps_by:
                #print "found"
                service_deps_by['selected'] = 1
            else:
                service_deps_by['selected'] = 0
            service_deps_by_list.append(service_deps_by)
            if service and service.name in service_to_update.deps_to:
                #print "found"
                service_deps_to['selected'] = 1
            else:
                service_deps_to['selected'] = 0
            service_deps_to_list.append(service_deps_to)

        #print service_deps_by_list
    
    context = {'service_deps_to_list': service_deps_to_list,'service_deps_by_list': service_deps_by_list,
               'services_list': services_list,'host_list': host_list,'service_selected':service_to_update,
               'message':message,'menu':menu_id,'tipi_servizio':tipi_servizio,'tipi_documentazione':tipi_documentazione}    
    #print request.POST
    if request.POST:
        service_to_update.name=request.POST['name']
        if service_to_update.host != request.POST['host']:
            prev_host = service_to_update.host
            print prev_host
        service_to_update.host=request.POST['host']
        service_to_update.port=request.POST['port']
        service_to_update.desc=request.POST['desc']
        service_to_update.svn=request.POST['svn']
        service_to_update.start=request.POST['start']
        service_to_update.stop=request.POST['stop']
        service_to_update.user=request.POST['user']
        service_to_update.deploy_doc_type = request.POST['deploy_doc_type']
        service_to_update.start_doc_type = request.POST['start_doc_type']
        service_to_update.stop_doc_type = request.POST['stop_doc_type']
        service_to_update.password=request.POST['password']
        service_to_update.deploy=request.POST['deploy']
        service_to_update.service_type=request.POST['service_type']
        service_to_update.documentation_url=request.POST['documentation_url']
        service_to_update.deps_by = request.POST.getlist('deps_by')
        service_to_update.deps_to = request.POST.getlist('deps_to')
        #service_to_update.save()
        #Aggiornamento delle dipendenze tra i servizi
        check_loop_dep = [dep_to for dep_to in service_to_update.deps_to if dep_to in service_to_update.deps_by]
        print len(check_loop_dep)
        if len(check_loop_dep) > 0 :
            print 'esco'
            context["message"]="Errore: aggiunta dipendenza circolare"
            #context["user_data"] = request.POST
            return render(request, 'services/update_service.html', context)
        else:
            deps_post_to = request.POST.getlist('deps_to')
            deps_post_by = request.POST.getlist('deps_by')
            if deps_post_to:
                dependencies_link(service_to_update_deps_to_before,service_to_update,deps_post_to,'TO')
            if deps_post_by:
                dependencies_link(service_to_update_deps_by_before,service_to_update,deps_post_by,'BY')        
        
        #     if deps_to:
        #         print 'Presenti dipendenze_to'
        #         service.deps_to = deps_to
        #         dependencies_link_add(service,deps_to,'TO')
        #         print 'dipendenza to aggunta'
        #     if deps_by:
        #         print 'Presenti dipendenze_by'
        #         service.deps_by = deps_by
        #         dependencies_link_add(service,deps_to,'BY')
        #         print 'dipendenza by aggunta'
        # context["message"]="Servizio aggiunto"
        service_to_update.save()
        #Rimuovo il servizio dall'host in cui stava se  cambiato
        host_to_update_del = Host.objects.get(name=prev_host)
        print host_to_update_del.services
        print service_to_update.name
        host_to_update_del.services.remove(service_to_update.name)
        host_to_update_del.save()
        host_to_update = Host.objects.get(name=service_to_update.host)
        host_to_update.services.append(service_to_update.name)
        host_to_update.save()
        context["message"] = "Servizio modificato"

    return render(request, 'services/update_service.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def service_delete(request,id):
    services_list = Service.objects.all()
    host_list = Host.objects.all()
    menu_id='service_mgt'
    service = get_or_none(Service,id=id)
    if service is None:
        message="Servizio non esistente"       
    else:
        deps_by_to_delete = service.deps_by
        deps_to_to_delete = service.deps_to
        print deps_by_to_delete
        print deps_to_to_delete
        dep_delete('BY',service,deps_by_to_delete)
        dep_delete('TO',service,deps_to_to_delete)
        host_to_update_del = Host.objects.get(name=service.host)
        host_to_update_del.services.remove(service.name)
        host_to_update_del.save()
        service.delete()
        message="Servizio eliminato"    
    context = {'services_list': services_list,'host_list': host_list,'message':message,'menu':menu_id}
    return render(request, 'services/delete_service.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser,login_url='/login/')
def host_add(request):
    message=""
    services_list = Service.objects.all()
    host_list = Host.objects.all()
    if request.POST:
        name=request.POST['name']
        ip=request.POST['ip']
        desc=request.POST['desc']
        services = request.POST.getlist('services')
        host=Host(name=name,services=services,IP=ip,desc=desc)
        host.save()
        message="Host aggiunto"
    menu_id='hosts_mgt'
    context = {'services_list': services_list,'host_list': host_list,'menu':menu_id,'message':message}
    return render(request, 'services/add_host.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser,login_url='/login/')
def host_update(request,id):
    host = Host.objects.get(id=id)
    message=""
    if request.POST:
        host.name=request.POST['name']
        host.IP=request.POST['ip']
        host.desc=request.POST['desc']
        host.services = request.POST.getlist('services')
        #host=Host(name=name,services=services,IP=ip,desc=desc)
        host.save()
        message="Host modificato"
    services_list = Service.objects.all()
    host_list = Host.objects.all()
    
    #print host.services
    host_services_list=[]
    for service in services_list:
        host_service = {}
        host_service['name'] = service.name
        if service and service.name in host.services:
            #print "found"
            host_service['selected'] = 1
        else:
            host_service['selected'] = 0
        host_services_list.append(host_service)
    menu_id='hosts_mgt'       
    #print host_services_list       
    context = {'host_services_list': host_services_list,'services_list': services_list,'host_list': host_list,'host_selected':host,'message':message,'menu':menu_id}
    #print message
    return render(request, 'services/update_host.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def host_delete(request,id):
    services_list = Service.objects.all()
    host_list = Host.objects.all()
    menu_id='hosts_mgt'
    host = get_or_none(Host,id=id)
    #host = Host.objects.get(id=id)
    if host is None:
        message="Host non esistente"       
    else:
        #print host.services
        for service_to_delete in host.services:
            print service_to_delete
            service = get_or_none(Service,name=service_to_delete)
            print "Servizio: " + service.name
            print service.deps_to
            print service.deps_by
            dep_delete('BY',service_to_delete,service.deps_by)
            dep_delete('TO',service_to_delete,service.deps_to)
            service.delete()
        host.delete()
        message="Host eliminato"
    context = {'services_list': services_list,'host_list': host_list,'message':message,'menu':menu_id}
    return render(request, 'services/delete_host.html', context)






