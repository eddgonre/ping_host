import tkinter as tk
from ping3 import ping
import threading
import time

# Lista de IPs o nombres de host a los que se hará ping
hosts = [
    {"name": "Google", "ip": "8.8.8.8"},
    {"name": "Open DNS", "ip": "208.67.222.222"},
    {"name": "Kolbi DNS", "ip": "181.193.94.94"},
    {"name": "Amazon", "ip": "www.amazon.com"},
    {"name": "Complejo Wilmer Lopez", "ip": "192.168.137.100"},
    {"name": "Tarimas Economicas", "ip": "192.168.137.101"},
    {"name": "Del Pino", "ip": "192.168.137.102"},
    {"name": "Litbo", "ip": "192.168.137.108"},
    {"name": "Estadio Rafael Bolaños", "ip": "192.168.137.120"},
    {"name": "COHOUSING", "ip": "192.168.137.112"},
    {"name": "Aserradero", "ip": "192.168.137.126"},
    {"name": "Pinalbo", "ip": "192.168.137.127"},
    {"name": "Casa Lidiethe", "ip": "192.168.137.128"},
    {"name": "Casa KIKO", "ip": "192.168.137.132"},
]

# Variable para controlar el número de ronda
round_number = 1

# Función para realizar ping secuencialmente a cada host
def ping_hosts_sequentially():
    global round_number  # Declarar la variable como global
    while not stop_event.is_set():
        for i, host_info in enumerate(hosts):
            try:
                response = ping(host_info['ip'], timeout=2)
                if response is not None:
                    labels[i].config(bg="green", text=f"{host_info['name']} ({host_info['ip']})")
                else:
                    labels[i].config(bg="white", text=f"{host_info['name']} ({host_info['ip']})")
            except Exception as e:
                labels[i].config(bg="orange", text=f"Error en {host_info['name']}: {str(e)}")

            # Espera 2 segundos para la primera ronda, 30 segundos después
            if round_number == 1:
                time.sleep(1)
            else:
                time.sleep(30)

        round_number += 1  # Aumentar el número de ronda después de terminar

# Función para detener el programa
def stop_ping():
    stop_event.set()
    root.quit()

# Configurar la ventana principal
root = tk.Tk()
root.title("Monitor de Ping")

# Centrar la ventana en la pantalla
window_width = 400
window_height = len(hosts) * 41  # Altura basada en el número de hosts
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.attributes("-topmost", True)  # Asegurar que la ventana esté enfrente

# Crear una variable de evento para detener los hilos
stop_event = threading.Event()

# Crear etiquetas dinámicas para cada host
labels = []
for host_info in hosts:
    label = tk.Label(root, text=f"Haciendo ping a {host_info['name']}...", width=50, height=2, bg="white")
    label.grid(row=len(labels), column=0)
    labels.append(label)

# Variable para controlar el número de ronda
round_number = 1

# Iniciar un hilo para hacer ping a los hosts secuencialmente
thread = threading.Thread(target=ping_hosts_sequentially, daemon=True)
thread.start()

# Botón para detener el monitor
stop_button = tk.Button(root, text="Detener", command=stop_ping)
stop_button.grid(row=len(hosts), column=0)

# Iniciar la interfaz gráfica
root.mainloop()
