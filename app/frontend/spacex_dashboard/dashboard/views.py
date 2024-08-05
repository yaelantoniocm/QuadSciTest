import requests
from django.shortcuts import render, redirect
from .tables import LaunchTable, RocketTable, StarlinkTable
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.ticker import MaxNLocator

def generate_bar_chart(data):
    fig, ax = plt.subplots()

    categories = ['Failed Launches', 'Successful Launches', 'Total Launches', 'Avg Launches Per Year']
    values = [
        data['failed_launches'],
        data['successful_launches'],
        data['total_launches'],
        data['avg_launches_per_year']
    ]

    ax.bar(categories, values, color=['red', 'green', 'blue', 'orange'])
    ax.set_title('Launch Statistics')
    ax.set_xlabel('')
    ax.set_ylabel('Count')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # Ensure y-axis has integer ticks

    # Remove x-axis labels to avoid clutter
    ax.set_xticklabels([])

    # Adjust the position of the bar chart to the right
    fig.subplots_adjust(left=0.2, right=0.9, top=0.8, bottom=0.2)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return image_base64

def generate_pie_chart(data):
    fig, ax = plt.subplots()

    labels = ['Active Satellites', 'Decayed Satellites']
    sizes = [
        data['active_satellites'],
        data['decayed_satellites']
    ]

    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
    ax.set_title('Starlink Satellite Statistics')
    ax.axis('equal')

    # Remove the legend from the chart
    ax.legend().set_visible(False)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return image_base64

def dashboard_view(request):
    response = requests.get('http://localhost:5001/api/dashboard')
    data = response.json()

    # Crear las tablas pasando una lista con un solo diccionario
    launch_table = LaunchTable([data['launches']])
    rocket_table = RocketTable([data['rockets']])
    starlink_table = StarlinkTable([data['starlink']])

    # Generar gráficos
    bar_chart = generate_bar_chart(data['launches'])
    pie_chart = generate_pie_chart(data['starlink'])

    context = {
        'launch_table': launch_table,
        'rocket_table': rocket_table,
        'starlink_table': starlink_table,
        'bar_chart': bar_chart,
        'pie_chart': pie_chart,
    }

    return render(request, 'dashboard/dashboard.html', context)

def home_view(request):
    return redirect('dashboard')
