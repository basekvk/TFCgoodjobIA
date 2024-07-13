import os
from scripts.capture_traffic import capture_traffic
from scripts.preprocess_data import pcap_to_dataframe
from scripts.train_model import train_model
from scripts.real_time_detection import real_time_detection
import logging

# Configuración del logging para mostrar colores en la consola
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_msg = super().format(record)
        if record.levelno == logging.INFO and "GoodJobs" in log_msg:
            return f"\033[91m{log_msg}\033[0m"  # Rojo
        return log_msg

logging.basicConfig(level=logging.INFO)
formatter = CustomFormatter('%(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.getLogger().handlers = [handler]

def main():
    try:
        # Capturar tráfico de red
        logging.info("Iniciando captura de tráfico de red...")
        capture_traffic()
        logging.info("Captura de tráfico completada.")
        
        # Preprocesar los datos capturados
        logging.info("Iniciando preprocesamiento de datos...")
        for batch_df in pcap_to_dataframe('data/captured_packets.pcap'):
            batch_df.to_csv('data/captured_packets_batch.csv', mode='a', header=False, index=False)
            logging.info("Procesado un lote de paquetes.")
        logging.info("Preprocesamiento de datos completado.")
        
        # Entrenar el modelo (puedes comentar esta línea si ya tienes un modelo entrenado)
        logging.info("Iniciando entrenamiento del modelo...")
        train_model()
        logging.info("Entrenamiento del modelo completado.")
        
        # Ejecutar la detección en tiempo real
        logging.info("Iniciando detección en tiempo real...")
        real_time_detection()
        logging.info("Detección en tiempo real completada.")
        
        # Mensaje final
        logging.info("Script creado para el TFC del Módulo 3 de IA de la Fundación GoodJobs, realizado por David García Algora. ¡Gracias por su atención!")
    except Exception as e:
        logging.error(f"Ocurrió un error en el proceso principal: {e}")

if __name__ == "__main__":
    main()
