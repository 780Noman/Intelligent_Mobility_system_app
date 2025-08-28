import subprocess
import sys
import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def run_neat_simulation(request):
    return render(request, 'simulation_notice.html')

def run_ddqn_simulation(request):
    return render(request, 'simulation_notice.html')