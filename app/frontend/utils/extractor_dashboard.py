import pandas as pd
import requests

# Hacer la llamada a la función get_dashboard
response = requests.get('http://localhost:5001/api/dashboard')

# Asegurarse de que la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()
    
    # Convertir los datos en dataframes de pandas
    launches_df = pd.DataFrame([data['launches']])
    rockets_df = pd.DataFrame([data['rockets']])
    starlink_df = pd.DataFrame([data['starlink']])
    
    # Mostrar los dataframes
    print("Launches DataFrame:")
    launches_df
    
    print("\nRockets DataFrame:")
    rockets_df
    
    print("\nStarlink DataFrame:")
    starlink_df
else:
    print(f"Error: {response.status_code}")
