from django.shortcuts import render

from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Create your views here.
def home_screen(request):
    #emplate = loader.get_template('base.html')
    #context = RequestContext(request, {'posts': posts})
    #body = template.render()
    return HttpResponse(base.html, content_type="text/html")

def results_screen(request):
    pass

def error_screen(request):
    pass