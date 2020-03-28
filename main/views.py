from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, "index.html", {"title": "Home"})


class SymptomsView(View):
    def get(self, request):
        return render(request, "index.html", {"title": "Home"})


class SpreadView(View):
    def get(self, request):
        return render(request, "index.html", {"title": "Home"})
