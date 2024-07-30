import taipy as tp
from taipy.gui import Gui, Markdown
import pandas as pd

# Crear un DataFrame simple
data = pd.DataFrame({
    'Category': ['A', 'B', 'C'],
    'Values': [10, 20, 30]
})

# Definir la interfaz de usuario
markdown = """
# Mi Aplicación con Taipy

```<|{data}|chart|type=bar|x=Category|y=Values|>```
"""

# Crear y mostrar la aplicación
gui = Gui(page=Markdown(markdown))
gui.run(port=5000)