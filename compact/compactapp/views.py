from django.shortcuts import render

from django.template import Context, loader, Template
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import SimpleAnalysis
from .forms import AdvancedAnalysis
import json


# Create your views here.
def home(request):
    """Home page - presents the user with the blank forms"""

    simple_analysis = SimpleAnalysis()
    advanced_analysis = AdvancedAnalysis()

    return render(request, 'base.html', {'simple_analysis': simple_analysis, 'advanced_analysis': advanced_analysis})

def results_simple(request):

    """Results page - presents the user with the output of the impact analysis model"""
    if request.method == 'POST':
        #create a form instance and populate it with data from the request
        try:
            simple_analysis = SimpleAnalysis(request.POST)
            if simple_analysis.is_valid():
                #TODO replace this with getting output and rendering
                return render(request, 'results_simple.html', {'simple_analysis': simple_analysis})
        except:
            return HttpResponseRedirect('error')
    else:
        #Temporary code to practice rendering results
        #TODO remove this shit

            #experimenting with searching and rendering sample output
        test_file = open("test_output.json")
        raw_output = test_file.read()
        my_dict = json.loads(raw_output)
        searched_id = '113FF'
        dummy_data = []

        for item in my_dict[2:len(my_dict)]:
            for key, value in item.items():
                if key == "ID" and searched_id in value:
                    dummy_data = item

        #json_table = json2html.convert(json = my_dict)
        return render(request, 'results_simple.html', {'results':dummy_data})
        
def results_advanced(request):

    """Results page - presents the user with the output of the impact analysis model"""
    if request.method == 'POST':
        #create a form instance and populate it with data from the request
        try:
            advanced_analysis = AdvancedAnalysis(request.POST)

            if advanced_analysis.emp_based_lc == True and advanced_analysis.wage_based_lc == True:
                return HttpResponseRedirect('error')

            if advanced_analysis.is_valid():
                #TODO replace this with getting output and rendering
                #results = complex_impact()
                return render(request, 'results_advanced.html', {'advanced_analysis': advanced_analysis})
                #
        except:
            return HttpResponseRedirect('error')
    else:
        #Temporary code to practice rendering results
        #TODO remove this shit

            #experimenting with searching and rendering sample output
        test_file = open("test_output.json")
        raw_output = test_file.read()
        my_dict = json.loads(raw_output)
        searched_id = '113FF'
        dummy_data = []

        for item in my_dict[2:len(my_dict)]:
            for key, value in item.items():
                if key == "ID" and searched_id in value:
                    dummy_data = item

        #json_table = json2html.convert(json = my_dict)
        return render(request, 'results_advanced.html', {'results':dummy_data})

    

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

