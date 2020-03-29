from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from m_statistics import data_analysis_1

# Create your views here.


class HomeView(View):
    def get(self, request):

        cases = data_analysis_1.get_cases()
        cases_obj = {
            "name": "Total Confirmed Cases",
            "number": cases,
            "style": "cases-color"
                     }

        deaths = data_analysis_1.get_deaths()
        deaths_obj = {
            "name": "Total Confirmed Deaths",
            "number": deaths,
            "style": "brand-color"
                     }

        recoveries = data_analysis_1.get_recoveries()
        recoveries_obj = {
            "name": "Total Confirmed Recoveries",
            "number": recoveries,
            "style": "recovered-color"
                     }

        return render(request, "index.html", {"title": "Home", "total_counts_covid": [cases_obj, deaths_obj, recoveries_obj]})


class SymptomsView(View):
    def get(self, request):
        return render(request, "index.html", {"title": "Home"})


class SpreadView(View):
    def get(self, request):
        return render(request, "index.html", {"title": "Home"})
