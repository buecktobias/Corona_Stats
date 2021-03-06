"""Corona_Stats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('symptoms/', SymptomsView.as_view(), name="symptoms"),
    path('about/', About.as_view(), name="about"),
    path('spread/', SpreadView.as_view(), name="spread"),
    path('prediction/', PredictionsView.as_view(), name="prediction"),
    path('api/zoom_countries/<int:zoom_level>', CoronaMap.as_view(), name="corona_map_zoom_level"),
    path('api/zoom_countries/', CoronaMap.as_view(), name="corona_map")
]
