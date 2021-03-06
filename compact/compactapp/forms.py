from django import forms
from compactapp.models import Area
import xlrd

class SimpleAnalysis(forms.Form):
    """"Provides the user with the Simple Analysis form."""

    areas = Area.objects.values('name')
    area_name = list(entry['name'] for entry in areas)
    #Gets all the US States from the database and puts them in a list.
    area_name.insert(0, 'US')
    #Appends the value "US" as this is not in the database, but is a valid input.
    area_number = list(range(0, len(area_name)))
    area_list = zip(area_number, area_name)
    #Zips all state names into a list of tuples, which is required to populate the dropdown menu.

    industry_file_location = "FinalNAICStoIOMatch.xlsx"
    workbook = xlrd.open_workbook(industry_file_location)
    sheet = workbook.sheet_by_name('NAICS to Sector')
    sector_ID = list(item for item in range(0,66))
    sector_description = list(item for item in sheet.col_values(1))
    sector_NAICS = list(item for item in sheet.col_values(3))
    #Gets NAICS and industry names from the excel sheet provided by Eric.

    industries = ["{} | NAICS Code {}".format(desc, int(NAICS)) for desc, NAICS in zip(sector_description, sector_NAICS)]
    industries = zip(sector_ID, industries)
    #Formats the menu item values for Industries and zips them into a list of tuples, which is required to populate the dropdown menu.

    year_choices = [2015]
    year_id = list(range(0, len(year_choices)))
    # This is so unpythonic, but is more scalable for when we add more years of data. Again, required to populate the dropdown menu. 


    industry = forms.ChoiceField(choices=industries)
    area = forms.ChoiceField(choices=area_list)
    year = forms.ChoiceField(choices=zip(year_id, year_choices))

class AdvancedAnalysis(forms.Form):

    areas = Area.objects.values('name')
    area_name = list(entry['name'] for entry in areas)
    area_name.insert(0, 'US')
    area_number = list(range(0, len(area_name)))
    area_list = zip(area_number, area_name)
    # Extremely unpythonic repetition of above code, however, Flask will not render the state list if I attempt to reuse the same code, because reasons

    year_choices = [2015]
    year_id = list(range(0, len(year_choices)))

    naics = forms.CharField(min_length=3, max_length=6, initial='111')
    area = forms.ChoiceField(choices=area_list)
    year = forms.ChoiceField(choices=zip(year_id, year_choices))
    revenue = forms.IntegerField(min_value=0, max_value=999999999999, initial=0)
    employees = forms.IntegerField(min_value=0, max_value=999999, initial=0)
    wages_annual = forms.IntegerField(min_value=0, max_value=999999999999, initial=0)
    emp_based_lc = forms.BooleanField(required=False)
    wage_based_lc = forms.BooleanField(required=False)