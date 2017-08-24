from django import forms
from compactapp.models import Area
import xlrd

class SimpleAnalysis(forms.Form):
    """"Provides the user with the Simple Analysis form."""

    areas = Area.objects.values('name')
    area_list = list(entry['name'] for entry in areas)
    area_list.insert(0, 'US')
    area_number = list(range(0, len(area_list)))
    area_list = zip(area_number, area_list)
    #Gets all Area objects and grabs the list of state names.
    #Appends the value "US" as this is not in the database, but is a valid input.
    #Zips all state names into a list of tuples so Django Forms can consume it.

    industry_file_location = "FinalNAICStoIOMatch.xlsx"
    workbook = xlrd.open_workbook(industry_file_location)
    sheet = workbook.sheet_by_name('NAICS to Sector')
    sector_ID = list(item for item in sheet.col_values(0))
    sector_description = list(item for item in sheet.col_values(1))
    sector_NAICS = list(item for item in sheet.col_values(3))
    #Gets all sector IDs, NAICS, and industry names from the excel sheet provided by Eric.

    industries = ["Sector ID: {} | {} | NAICS Code {}".format(int(ID), desc, int(NAICS)) for ID, desc, NAICS in zip(sector_ID, sector_description, sector_NAICS)]
    industries = zip(sector_ID, industries)
    #Formats the menu item choices for Industries and zips them into a list of tuples.


    industry = forms.ChoiceField(choices=industries)
    area = forms.ChoiceField(choices=area_list)
    year = forms.ChoiceField(choices=[(1, 2015)])

class AdvancedAnalysis(forms.Form):

    areas = Area.objects.values('name')
    area_list = list(entry['name'] for entry in areas)
    area_list.insert(0, 'US')
    area_number = list(range(0, len(area_list)))
    area_list = zip(area_number, area_list)
    # Extremely unpythonic repetition of above code, however, Flask will not render the state list if I attempt to reuse the same code, because reasons

    naics = forms.CharField(min_length=3, max_length=6, initial='111')
    area = forms.ChoiceField(choices=area_list)
    year = forms.ChoiceField(choices=[(1, 2015)])
    revenue = forms.IntegerField(min_value=0, max_value=999999999999, initial=0)
    employees = forms.IntegerField(min_value=0, max_value=999999, initial=0)
    wages_annual = forms.IntegerField(min_value=0, max_value=999999999999, initial=0)
    emp_based_lc = forms.BooleanField(required=False)
    wage_based_lc = forms.BooleanField(required=False)