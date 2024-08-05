from django.shortcuts import render

def rockets_launches_view(request):
    return render(request, 'rocket_launch_app/rockets_launches.html')
