
# Proyecto de Monitoreo de Tráfico de Red

Este proyecto captura, preprocesa, entrena un modelo y detecta anomalías en el tráfico de red en tiempo real. Fue creado como parte del TFC del Módulo 3 de IA de la Fundación GoodJobs, realizado por David García Algora. Este proyecto se ha hecho con fines educativos.

## Requisitos

- Docker
- Python 3.8 o superior (si decides ejecutar el script fuera de Docker)

## Configuración del Entorno

### Usando Docker

1. Clona este repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Construye la imagen de Docker:
    ```sh
    docker build -t red-monitor .
    ```

3. Ejecuta el contenedor:
    ```sh
    docker run -it --rm red-monitor
    ```

### Usando Python Localmente

1. Clona este repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Crea y activa un entorno virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Descarga el archivo `UNSW_NB15.csv`:
    - Puedes descargar el archivo `UNSW_NB15.csv` desde el siguiente enlace: [UNSW-NB15 Dataset](https://www.unsw.adfa.edu.au/unsw-canberra-cyber/cybersecurity/ADFA-NB15-Datasets/)

5. Coloca el archivo `UNSW_NB15.csv` en la carpeta `data`.

6. Ejecuta el script principal:
    ```sh
    python main.py
    ```

### Dependencias

Las principales dependencias de este proyecto son:

- pandas
- numpy
- scikit-learn
- joblib
- scapy

Asegúrate de que todas estén especificadas en `requirements.txt`.

### Notas Adicionales

Este proyecto utiliza `scapy` para capturar tráfico de red. Asegúrate de que `scapy` esté correctamente instalado y configurado. Si usas Docker, todas las dependencias se instalarán automáticamente.

### Mensaje Final

Al finalizar la ejecución, el script mostrará el siguiente mensaje en la consola:
Script creado para el TFC del Módulo 3 de IA de la Fundación GoodJobs, realizado por David García Algora. ¡Gracias por su atención!
Este mensaje confirma que el proceso ha concluido exitosamente.

---

**David García Algora**

**Proyecto realizado con fines educativos**

---

### Archivos del Proyecto

A continuación se presentan todos los archivos necesarios para el proyecto.

### Dockerfile

```Dockerfile
# Utilizar una imagen base oficial de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requerimientos al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al contenedor
COPY . .

# Comando para ejecutar el script principal
CMD ["python", "main.py"]
