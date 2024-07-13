import pandas as pd
import joblib
import logging
import os

logging.basicConfig(level=logging.INFO)

def real_time_detection():
    try:
        # Cargar el modelo entrenado y el preprocesador
        model_path = os.path.join('models', 'ids_model_unws_nb15.pkl')
        preprocessor_path = os.path.join('models', 'preprocessor.pkl')

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"El archivo de modelo {model_path} no fue encontrado.")
        if not os.path.exists(preprocessor_path):
            raise FileNotFoundError(f"El archivo del preprocesador {preprocessor_path} no fue encontrado.")

        model = joblib.load(model_path)
        preprocessor = joblib.load(preprocessor_path)

        # Cargar el archivo de datos capturados
        captured_data_path = 'data/captured_packets_batch.csv'
        if not os.path.exists(captured_data_path):
            raise FileNotFoundError(f"El archivo de datos capturados {captured_data_path} no fue encontrado.")

        df = pd.read_csv(captured_data_path)
        train_columns = joblib.load('models/train_columns.pkl')
        
        # Asegurar que todas las columnas esperadas están presentes
        for col in train_columns:
            if col not in df.columns:
                df[col] = None

        df = df[train_columns]

        # Preprocesar los datos
        X = preprocessor.transform(df)

        # Realizar predicciones
        predictions = model.predict(X)
        logging.info(f"Predicciones: {predictions}")
    except FileNotFoundError as e:
        logging.error(f"Archivo no encontrado: {e}")
    except Exception as e:
        logging.error(f"Error prediciendo el paquete: {e}")

if __name__ == "__main__":
    real_time_detection()
