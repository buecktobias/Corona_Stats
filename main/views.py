from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from m_statistics import data_analysis_1

# Create your views here.


class HomeView(View):
    def get_numbers(self):

        if data_analysis_1.DataAnalysis.get_instance() is None:
            data_analysis = data_analysis_1.DataAnalysis()
        else:
            data_analysis = data_analysis_1.DataAnalysis.get_instance()

        cases = data_analysis.get_cases()
        cases_obj = {
            "name": "Total Confirmed Cases",
            "number": cases,
            "style": "cases-color"
                     }

        deaths = data_analysis.get_deaths()
        deaths_obj = {
            "name": "Total Confirmed Deaths",
            "number": deaths,
            "style": "brand-color"
                     }

        recoveries = data_analysis.get_recoveries()
        recoveries_obj = {
            "name": "Total Confirmed Recoveries",
            "number": recoveries,
            "style": "recovered-color"
                     }

        active_cases = data_analysis.get_active_cases()
        active_cases_obj = {
            "name": "Total Confirmed Active Cases",
            "number": active_cases,
            "style": "active-cases-color"
                     }
        return [cases_obj, deaths_obj, recoveries_obj, active_cases_obj]

    def get_plots(self):
        if data_analysis_1.DataAnalysis.get_instance() is None:
            data_analysis = data_analysis_1.DataAnalysis()
        else:
            data_analysis = data_analysis_1.DataAnalysis.get_instance()

        def get_part_after_static(file_path):
            after_static_part = file_path.split("static/")[-1]
            return after_static_part

        active_cases_plot_file = data_analysis.ACTIVE_CASES_PLOT_FILE
        cases_plot_file = data_analysis.CASES_PLOT_FILE
        recoveries_plot_file = data_analysis.RECOVERIES_PLOT_FILE
        deaths_plot_file = data_analysis.DEATHS_PLOT_FILE

        file_paths = [cases_plot_file, deaths_plot_file, recoveries_plot_file, active_cases_plot_file]

        file_paths_after_static = list(map(get_part_after_static, file_paths))
        return file_paths_after_static

    def get(self, request):
        return render(request, "index.html", {
            "title": "Home",
            "total_counts_covid": self.get_numbers(),
            "plot_files": self.get_plots()
          })


class SymptomsView(View):
    def get(self, request):
        return render(request, "index.html", {"title": "Home"})


class SpreadView(View):
    def get(self, request):
        return render(request, "index.html", {"title": "Home"})
