from django.db import models
from djangotoolbox.fields import ListField
from .forms import StringListField
from django import forms


class CategoryField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)
        
class Host(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    IP = models.CharField(max_length=100, blank=True)
    services = CategoryField(blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        

class Service(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=100,blank=True)
    port = models.CharField(max_length=100,blank=True)
    service_type = models.CharField(max_length=100,blank=True)
    desc = models.TextField(blank=True)
    documentation_url = models.CharField(max_length=100,blank=True)
    svn = models.CharField(max_length=100,blank=True)
    deploy = models.TextField(blank=True)
    deps_to = CategoryField(blank=True)
    deps_by = CategoryField(blank=True)
    user = models.CharField(max_length=100,blank=True)
    password = models.CharField(max_length=100,blank=True)
    start = models.CharField(max_length=100,blank=True)
    stop = models.CharField(max_length=100,blank=True)
    start_doc_type = models.CharField(max_length=100,blank=True)
    stop_doc_type = models.CharField(max_length=100,blank=True)
    deploy_doc_type = models.CharField(max_length=100,blank=True)

   
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

