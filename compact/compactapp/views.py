from django.shortcuts import render

from django.template import Context, loader, Template
from django.http import HttpResponse, HttpResponseRedirect, Http404
from compactapp.models import Area

import xlrd
import itertools

# Create your views here.
def home(request):
    template = loader.get_template('base.html')
    areas = Area.objects.values('name')
    area_list = list(entry['name'] for entry in areas)

    industry_file_location = "FinalNAICStoIOMatch.xlsx"
    workbook = xlrd.open_workbook(industry_file_location)
    sheet = workbook.sheet_by_name('NAICS to Sector')
    sector_ID = list(item for item in sheet.col_values(0))
    sector_description = list(item for item in sheet.col_values(1))
    del sector_description[0]
    sector_NAICS = list(item for item in sheet.col_values(3))
    del sector_NAICS[0]
    del sector_NAICS[-1]
    industries = ["{} - NAICS Code: {}".format(desc, int(NAICS)) for desc, NAICS in zip(sector_description, sector_NAICS)]

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