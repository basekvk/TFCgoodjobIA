import pandas as pd
from scapy.all import rdpcap
import logging
import os
import joblib

logging.basicConfig(level=logging.INFO)

def pcap_to_dataframe(pcap_file, batch_size=1000):
    try:
        if not os.path.isfile(pcap_file):
            logging.error(f"Archivo no encontrado en la ruta: {pcap_file}")
            return

        packets = rdpcap(pcap_file)
        rows = []
        for i, packet in enumerate(packets):
            try:
                row = {
                    'id': None,
                    'dur': None,
                    'proto': packet[1].proto if hasattr(packet[1], 'proto') else None,
                    'service': None,
                    'state': None,
                    'spkts': None,
                    'dpkts': None,
                    'sbytes': None,
                    'dbytes': None,
                    'rate': None,
                    'sttl': packet[1].ttl if hasattr(packet[1], 'ttl') else None,
                    'dttl': None,
                    'sload': None,
                    'dload': None,
                    'sloss': None,
                    'dloss': None,
                    'sinpkt': None,
                    'dinpkt': None,
                    'sjit': None,
                    'djit': None,
                    'swin': None,
                    'stcpb': None,
                    'dtcpb': None,
                    'dwin': None,
                    'tcprtt': None,
                    'synack': None,
                    'ackdat': None,
                    'smean': None,
                    'dmean': None,
                    'trans_depth': None,
                    'response_body_len': None,
                    'ct_srv_src': None,
                    'ct_state_ttl': None,
                    'ct_dst_ltm': None,
                    'ct_src_dport_ltm': None,
                    'ct_dst_sport_ltm': None,
                    'ct_dst_src_ltm': None,
                    'is_ftp_login': None,
                    'ct_ftp_cmd': None,
                    'ct_flw_http_mthd': None,
                    'ct_src_ltm': None,
                    'ct_srv_dst': None,
                    'is_sm_ips_ports': None
                }
                rows.append(row)
            except IndexError as e:
                logging.warning(f"Paquete no tiene el índice esperado: {e}")
            except AttributeError as e:
                logging.error(f"Error preprocesando el paquete: {e}")

            if len(rows) >= batch_size:
                yield pd.DataFrame(rows)
                rows = []
        if rows:
            yield pd.DataFrame(rows)
    except Exception as e:
        logging.error(f"Error procesando el archivo pcap: {e}")

if __name__ == "__main__":
    try:
        train_columns = joblib.load('models/train_columns.pkl')
        
        # Limpiar el archivo existente
        captured_data_path = 'data/captured_packets_batch.csv'
        if os.path.exists(captured_data_path):
            os.remove(captured_data_path)
        
        for batch_df in pcap_to_dataframe('data/captured_packets.pcap'):
            # Asegurar que las columnas coinciden con las utilizadas en el entrenamiento
            for col in train_columns:
                if col not in batch_df.columns:
                    batch_df[col] = None
            batch_df = batch_df[train_columns]
            
            if not os.path.exists(captured_data_path):
                batch_df.to_csv(captured_data_path, mode='w', header=True, index=False)
            else:
                batch_df.to_csv(captured_data_path, mode='a', header=False, index=False)
            
            logging.info("Procesado un lote de paquetes.")
        logging.info("Preprocesamiento de datos completado.")
    except Exception as e:
        logging.error(f"Error en el preprocesamiento de datos: {e}")
