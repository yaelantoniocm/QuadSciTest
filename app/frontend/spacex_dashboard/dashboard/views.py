import requests
from django.shortcuts import render, redirect
from .tables import LaunchTable, RocketTable, StarlinkTable

def dashboard_view(request):
    response = requests.get('http://localhost:5001/api/dashboard')
    data = response.json()

    # Crear las tablas pasando una lista con un solo diccionario
    launch_table = LaunchTable([data['launches']])
    rocket_table = RocketTable([data['rockets']])
    starlink_table = StarlinkTable([data['starlink']])

    context = {
        'launch_table': launch_table,
        'rocket_table': rocket_table,
        'starlink_table': starlink_table,
    }

    return render(request, 'dashboard.html', context)


def home_view(request):
    return redirect('dashboard')
