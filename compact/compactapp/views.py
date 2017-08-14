from django.shortcuts import render

from django.template import Context, loader, Template
from django.http import HttpResponse, HttpResponseRedirect, Http404
from compactapp.models import Area

# Create your views here.
def home(request):
    template = loader.get_template('base.html')
    areas = Area.objects.values('name')
    industries = [
    "Production", 
    "Utilities", 
    "Construction", 
    "Nondurables Manufacturing", 
    "Durables Manufacturing", 
    "Wholesale and Retail", 
    "Transporation", 
    "Info & Telecom", 
    "Finance, Insurance, Rental, and Real Estate",
    "Professional Services",
    "Health Services", 
    "Other Services", 
    "Food Services"
    ]
    area_list = list(entry['name'] for entry in areas)

    context = {'areas': areas, 'industries': industries}

    return render(request, 'base.html', context)

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