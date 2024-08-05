import matplotlib.pyplot as plt
import pandas as pd
import os
import requests

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def generate_charts():
    # Ruta absoluta para la carpeta static/images
    static_dir = os.path.join(os.path.dirname(__file__), 'spacex_dashboard/static/images')

    # Fetch data from API
    rockets_response = requests.get('http://localhost:5001/api/rockets')
    launches_response = requests.get('http://localhost:5001/api/launches')
    
    rockets_data = rockets_response.json()
    launches_data = launches_response.json()
    
    # Prepare rockets DataFrame
    rockets_df = pd.DataFrame(rockets_data)
    
    # Rocket success comparison
    plt.figure(figsize=(10, 6))
    plt.bar(rockets_df['name'], rockets_df['success_rate_pct'], color='skyblue')
    plt.xlabel('Rocket Models')
    plt.ylabel('Success Rate (%)')
    plt.title('Success Rate Comparison of Rocket Models')
    plt.savefig(os.path.join(static_dir, 'rocket_success_comparison.png'))
    plt.close()

    # Rocket cost comparison
    plt.figure(figsize=(10, 6))
    plt.bar(rockets_df['name'], rockets_df['cost_per_launch'], color='salmon')
    plt.xlabel('Rocket Models')
    plt.ylabel('Cost per Launch ($)')
    plt.title('Launch Cost Comparison of Rockets')
    plt.ylim(0, rockets_df['cost_per_launch'].max() * 1.2)  # Adjust the y-axis
    plt.savefig(os.path.join(static_dir, 'rocket_cost_comparison.png'))
    plt.close()

    # Rocket weight comparison
    plt.figure(figsize=(10, 6))
    plt.bar(rockets_df['name'], rockets_df['mass_kg'], color='orange')
    plt.xlabel('Rocket Models')
    plt.ylabel('Weight (kg)')
    plt.title('Weight Comparison of Rockets')
    plt.ylim(0, rockets_df['mass_kg'].max() * 1.2)  # Adjust the y-axis
    plt.savefig(os.path.join(static_dir, 'rocket_weight_comparison.png'))
    plt.close()

    # Prepare launches DataFrame
    launches_df = pd.DataFrame(launches_data)
    launches_df['date_utc'] = pd.to_datetime(launches_df['date_utc'])
    launches_df['year'] = launches_df['date_utc'].dt.year

    # Launch success rate per year
    launches_df['success'] = launches_df['success'].map({'true': True, 'false': False, 'none': False})
    success_rate_per_year = launches_df.groupby('year')['success'].mean() * 100

    plt.figure(figsize=(10, 6))
    plt.plot(success_rate_per_year.index, success_rate_per_year.values, marker='o', linestyle='-', color='green')
    plt.xlabel('Year')
    plt.ylabel('Success Rate (%)')
    plt.title('Launch Success Rate Per Year')
    plt.savefig(os.path.join(static_dir, 'launch_success_rate_per_year.png'))
    plt.close()

if __name__ == "__main__":
    generate_charts()