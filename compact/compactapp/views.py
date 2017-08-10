from django.shortcuts import render

from django.template import Context, loader, Template
from django.http import HttpResponse, HttpResponseRedirect, Http404
from compactapp.models import Area

# Create your views here.
def home_screen(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render())

def results_screen(request):
    pass

def error_screen(request):
    pass