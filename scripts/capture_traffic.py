from scapy.all import sniff, wrpcap
import logging

logging.basicConfig(level=logging.INFO)

def packet_callback(packet):
    logging.info(packet.show())

def capture_traffic(output_file='data/captured_packets.pcap', packet_count=100):
    try:
        # Captura 100 paquetes de la interfaz de red
        packets = sniff(count=packet_count, prn=packet_callback)
        # Guarda los paquetes capturados en un archivo pcap
        wrpcap(output_file, packets)
        logging.info(f"Capturados {packet_count} paquetes.")
    except PermissionError:
        logging.error("Permiso denegado: Por favor ejecuta como superusuario.")
    except Exception as e:
        logging.error(f"Error capturando tráfico: {e}")

if __name__ == "__main__":
    capture_traffic()
