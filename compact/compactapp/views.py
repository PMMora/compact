from django.shortcuts import render

from django.template import Context, loader, Template
from django.http import HttpResponse, HttpResponseRedirect, Http404
from compactapp.models import Area

# Create your views here.
def home_screen(request):
    options = []
    template = loader.get_template('base.html')
    return HttpResponse(template.render())

def results(request):
    template = loader.get_template('results.html')
    return HttpResponse(template.render())

def error_page(request):
    template = loader.get_template('error_page.html')
    return HttpResponse(template.render())