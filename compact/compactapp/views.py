from django.shortcuts import render

from django.template import Context, loader, Template
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import SimpleAnalysis
from .forms import AdvancedAnalysis
from .economicimpact import simple_impact
from .economicimpact import complex_impact

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
        completed_form = SimpleAnalysis(request.POST)

        simple_analysis = SimpleAnalysis()

        if completed_form.is_valid():
            #Get searched industry, name, and year from the form
            searched_industry_index = int(completed_form.cleaned_data['industry'])
            searched_industry = simple_analysis.sector_description[searched_industry_index]
            searched_area = simple_analysis.area_name[int(completed_form.cleaned_data['area'])]
            searched_year = simple_analysis.year_choices[int(completed_form.cleaned_data['year'])]
            #Run the impact analysis model with the searched values from the form.
            results = simple_impact(user_input=[str(searched_area),searched_year,searched_industry_index])

            #Get totals of each field for chart - iterating through dict at template level highly affected latency
            direct_revenue = 0
            direct_employment = 0
            direct_wage = 0
            indirect_revenue = 0
            indirect_employment = 0
            indirect_wage = 0
            induced_revenue = 0
            induced_employment = 0
            induced_wage = 0


            for dictionary in results:
                direct_revenue += dictionary['direct_rev']
                direct_employment += dictionary['direct_emp']
                direct_wage += dictionary['direct_wage']
                indirect_revenue += dictionary['indirect_rev']
                indirect_employment += dictionary['indirect_emp']
                indirect_wage += dictionary['indirect_wage']
                induced_revenue += dictionary['induced_rev']
                induced_employment += dictionary['induced_emp']
                induced_wage += dictionary['induced_wage']

        else:
            results = "Unavailable"
            searched_industry = "Unavailable"
            searched_area = "Unavailable"

        return render(request, 'results_simple.html', {
            'simple_analysis': simple_analysis, 
            'results': results, 
            'searched_industry': searched_industry, 
            'searched_area': searched_area, 
            'searched_year': searched_year,
            'direct_revenue': direct_revenue,
            'direct_employment': direct_employment,
            'direct_wage': direct_wage,
            'indirect_revenue': indirect_revenue,
            'indirect_wage': indirect_wage,
            'indirect_employment': indirect_employment,
            'induced_revenue': induced_revenue,
            'induced_employment': induced_employment,
            'induced_wage': induced_wage,
            }
            )

    else:
        return HttpResponseRedirect('/error_page')
        
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

