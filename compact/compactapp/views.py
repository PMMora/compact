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
        #create a blank form instance to use for populating label of user-selected choices
        simple_analysis = SimpleAnalysis()

        if completed_form.is_valid():
            #Get searched industry, name, and year from the form
            industry_index = int(completed_form.cleaned_data['industry'])
            industry = simple_analysis.sector_description[industry_index]
            area = simple_analysis.area_name[int(completed_form.cleaned_data['area'])]
            year = simple_analysis.year_choices[int(completed_form.cleaned_data['year'])]
            #Run the impact analysis model with the searched values from the form.
            results = simple_impact(user_input=[str(area),year,industry_index])

            #Get totals of each field for chart - iterating through dict at template level highly affected latency
            #TODO create function to parse dictionaries, and replace this chunk of code below
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

        return render(request, 'results_simple.html', {
            'simple_analysis': simple_analysis, 
            'results': results, 
            'industry': industry, 
            'area': area, 
            'year': year,
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
    #If request_method != POST, return error
    else:
        return HttpResponseRedirect('/error_page')


def results_advanced(request):
    """Results page - presents the user with the output of the impact analysis model"""
    if request.method == "POST":
        #create a form instance and populate it with data from the request
        completed_form = AdvancedAnalysis(request.POST)
        #create a blank form instance to use for populating label of user-selected choices
        advanced_analysis = AdvancedAnalysis()


        if completed_form.is_valid():
            #Get searched industry, name, and year from the form
            naics = int(completed_form.cleaned_data['naics'])
            area = advanced_analysis.area_name[int(completed_form.cleaned_data['area'])]
            year = advanced_analysis.year_choices[int(completed_form.cleaned_data['year'])]
            revenue = completed_form.cleaned_data['revenue']
            employees = completed_form.cleaned_data['employees']
            wages = completed_form.cleaned_data['wages_annual']
            LQ_display = ""
            LQ_type = ""

            #Checks for additional options
            if completed_form.cleaned_data['emp_based_lc'] == True and completed_form.cleaned_data['wage_based_lc'] == True:
                return HttpResponseRedirect('/error_page')
            elif completed_form.cleaned_data['emp_based_lc'] == True:
                LQ_type = "employees"
                LQ_display = "Employee-Based"
            else:
                LQ_type = "wages"
                LQ_display = "Wage-Based"

            #Run the impact analysis model with the searched values from the form.
            results = complex_impact(user_input=[str(area),year,[naics, employees, revenue, wages], LQ_type])

            #Get totals of each field for chart - iterating through dict at template level highly affected latency
            #TODO create function to parse dictionaries, and replace this chunk of code below
            
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
                
        return render(request, 'results_advanced.html', {
            'advanced_analysis': advanced_analysis,
            'results': results,
            'naics':naics,
            'area':area,
            'year':year,
            'revenue':revenue,
            'employees':employees,
            'wages': wages,
            'LQ_display': LQ_display,
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
        #If request_method != POST, return error
    else:
        return HttpResponseRedirect('/error_page')

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

