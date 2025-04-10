# 📊 Visualizador CSV con Gemini AI

Esta aplicación web permite cargar archivos CSV y generar visualizaciones de datos de forma interactiva utilizando la IA de Google Gemini. La aplicación está construida con Streamlit y permite personalizar gráficos de manera intuitiva a través de prompts en lenguaje natural.

## 🚀 Características

- Carga de archivos CSV
- Visualización previa de datos
- Generación de gráficos usando IA
- Personalización de visualizaciones
- Interfaz intuitiva
- Soporte para múltiples tipos de gráficos

## 📋 Requisitos Previos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)
- Una clave API de Google Gemini

## ⚙️ Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
```

2. Crea un entorno virtual:
```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` en la raíz del proyecto:
```bash
GEMINI_API_KEY=tu_clave_api_aquí
```

## 🎮 Uso

1. Activa el entorno virtual si no está activado:
```bash
# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

2. Ejecuta la aplicación:
```bash
streamlit run app.py
```

3. Abre tu navegador en `http://localhost:8501`

## 📝 Cómo Usar la Aplicación

1. **Carga de Datos**: 
   - Haz clic en "Choose a CSV file" en la barra lateral
   - Selecciona tu archivo CSV

2. **Visualización de Datos**:
   - Revisa la vista previa de los datos
   - Explora las estadísticas básicas
   - Verifica los tipos de datos

3. **Generación de Gráficos**:
   - Describe el gráfico que deseas en el área de texto
   - Haz clic en "Generate & Display Plot"
   - El código generado y el gráfico se mostrarán automáticamente

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## ⚠️ Notas Importantes

- Asegúrate de tener una clave API válida de Google Gemini
- Los archivos CSV deben estar correctamente formateados
- La aplicación funciona mejor con conjuntos de datos limpios y estructurados
