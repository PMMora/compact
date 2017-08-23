from django.shortcuts import render

from django.template import Context, loader, Template
from django.http import HttpResponse, HttpResponseRedirect, Http404
from compactapp.models import Area
from .forms import SimpleAnalysis
from .forms import AdvancedAnalysis

import xlrd


# Create your views here.
def home(request):
    template = loader.get_template('base.html')
    simple_analysis = SimpleAnalysis()
    advanced_analysis = AdvancedAnalysis()

    return render(request, 'base.html', {'simple_analysis': simple_analysis, 'advanced_analysis': advanced_analysis})

def results(request):

    template = loader.get_template('results.html')


    return HttpResponse(template.render())

def error_page(request):
    template = loader.get_template('error_page.html')
    return HttpResponse(template.render())

def about(request):
    template = loader.get_template('about.html')
    return HttpResponse(template.render())

def user_manual(request):
    template = loader.get_template('user_manual.html')
    return HttpResponse(template.render())

def faq(request):
    template = loader.get_template('faq.html')
    return HttpResponse(template.render())