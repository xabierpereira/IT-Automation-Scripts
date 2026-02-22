#!/usr/bin/env python3
"""
system_info_visual.py - Informe de sistema bonito y multiplataforma

Uso: python system_info_visual.py
Requisitos: pip install psutil
"""

import platform, psutil, socket, getpass, sys, subprocess
from datetime import datetime
import re

# Detectar SO
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# Archivo de salida
filename = f"informe_sistema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
f = open(filename, "w", encoding="utf-8")

# Función para imprimir y guardar
def print_save(text="", color=None):
    if color:
        print(color + text + "\033[0m")
        f.write(text + "\n")
    else:
        print(text)
        f.write(text + "\n")

# Función de barra visual
def bar_graph(value, max_value=100, length=30, color="\033[92m"):
    filled = int((value / max_value) * length)
    bar = "[" + "#" * filled + "-" * (length - filled) + "]"
    return f"{color}{bar} {value:.1f}%\033[0m"

# Colores ANSI
TITLE = "\033[95m"       # Magenta
SECTION = "\033[94m"     # Azul
HIGHLIGHT = "\033[93m"   # Amarillo
INFO = "\033[96m"        # Cyan

# Encabezado
print_save("=" * 70, TITLE)
print_save(f"{'INFORME SISTEMA MULTIPLATAFORMA':^70}", TITLE)
print_save(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^70}", TITLE)
print_save("=" * 70, TITLE)

# ========================= SISTEMA OPERATIVO =========================
print_save("\n[SISTEMA OPERATIVO]", SECTION)
print_save(f"OS: {platform.system()} {platform.release()}")
print_save(f"Versión: {platform.version()}")
print_save(f"Arquitectura: {platform.machine()}")
print_save(f"Hostname: {socket.gethostname()}")
print_save(f"Usuario: {getpass.getuser()}")
print_save(f"Python: {sys.version.split()[0]}")

# ========================= CPU / GPU =========================
def get_cpu_info():
    if IS_WINDOWS:
        try:
            return subprocess.check_output(
                ["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Processor).Name"],
                encoding="utf-8"
            ).strip()
        except:
            return "No disponible"
    elif IS_LINUX:
        try:
            with open("/proc/cpuinfo") as f_cpu:
                for line in f_cpu:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except:
            return "No disponible"

def get_gpu_info():
    if IS_WINDOWS:
        try:
            return subprocess.check_output(
                ["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_VideoController).Name"],
                encoding="utf-8"
            ).strip()
        except:
            return "No disponible"
    elif IS_LINUX:
        try:
            output = subprocess.check_output(["lspci"], encoding="utf-8")
            gpus = [line.split(":")[-1].strip() for line in output.splitlines() if "VGA" in line or "3D" in line]
            return ", ".join(gpus) if gpus else "No disponible"
        except:
            return "No disponible"

def get_gpu_vram():
    if IS_WINDOWS:
        try:
            output = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command",
                 "(Get-CimInstance Win32_VideoController | Select AdapterRAM | Format-List | Out-String)"],
                encoding="utf-8"
            ).replace("\r", "")
            nums = re.findall(r'\d+', output)
            return ", ".join(f"{int(n)//(1024**2)} GB" for n in nums) if nums else "No disponible"
        except:
            return "No disponible"
    elif IS_LINUX:
        try:
            output = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"], encoding="utf-8")
            nums = [line.strip() for line in output.splitlines() if line.strip()]
            return ", ".join(f"{int(n)//1024} GB" for n in nums) if nums else "No disponible"
        except:
            return "No disponible"

print_save("\n[PROCESADOR]", SECTION)
print_save(f"CPU: {get_cpu_info()}")
print_save(f"Núcleos físicos: {psutil.cpu_count(logical=False)}")
print_save(f"Núcleos lógicos: {psutil.cpu_count(logical=True)}")
cpu_percent = psutil.cpu_percent(interval=1)
print_save(f"Uso CPU: {cpu_percent}% {bar_graph(cpu_percent)}")

print_save("\n[GRÁFICOS]", SECTION)
print_save(f"GPU: {get_gpu_info()}")
print_save(f"GPU VRAM: {get_gpu_vram()}")

# ========================= MEMORIA =========================
print_save("\n[MEMORIA RAM]", SECTION)
ram = psutil.virtual_memory()
print_save(f"Total: {ram.total / (1024**3):.2f} GB")
print_save(f"Disponible: {ram.available / (1024**3):.2f} GB")
print_save(f"Usado: {ram.percent}% {bar_graph(ram.percent)}")

# ========================= ALMACENAMIENTO =========================
print_save("\n[ALMACENAMIENTO]", SECTION)
for partition in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(partition.mountpoint)
        print_save(f"\n{partition.device} ({partition.fstype})")
        print_save(f"  Total: {usage.total / (1024**3):.2f} GB")
        print_save(f"  Usado: {usage.used / (1024**3):.2f} GB ({usage.percent}%) {bar_graph(usage.percent)}")
        print_save(f"  Libre: {usage.free / (1024**3):.2f} GB")
    except:
        pass

# ========================= RED =========================
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "No disponible"

def get_wifi_name():
    if IS_WINDOWS:
        try:
            output = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], encoding="utf-8")
            for line in output.splitlines():
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()
        except:
            pass
    elif IS_LINUX:
        try:
            output = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"], encoding="utf-8")
            for line in output.splitlines():
                if line.startswith("yes:"):
                    return line.split(":")[1]
        except:
            pass
    return "No disponible"

def get_network_speed():
    stats = psutil.net_if_stats()
    for iface, data in stats.items():
        if data.isup and data.speed > 0:
            return f"{data.speed} Mbps"
    return "No disponible"

def get_active_network_adapter():
    stats = psutil.net_if_stats()
    for iface, data in stats.items():
        if data.isup and data.speed > 0:
            return iface
    return "No disponible"

print_save("\n[RED]", SECTION)
print_save(f"Adaptador activo: {get_active_network_adapter()}")
print_save(f"IP Local: {get_local_ip()}")
print_save(f"Red (SSID): {get_wifi_name()}")
print_save(f"Velocidad del enlace: {get_network_speed()}")

# ========================= BATERÍA =========================
battery = psutil.sensors_battery()
if battery:
    print_save("\n[BATERÍA]", SECTION)
    print_save(f"Nivel: {battery.percent}% {bar_graph(battery.percent)}")
    print_save(f"Enchufado: {'Sí' if battery.power_plugged else 'No'}")

# ========================= PLACA BASE =========================
def get_motherboard():
    if IS_WINDOWS:
        try:
            return subprocess.check_output(
                ["powershell", "-NoProfile", "-Command",
                 "(Get-CimInstance Win32_BaseBoard | Select Manufacturer, Product | Format-List | Out-String)"],
                encoding="utf-8"
            ).replace("\r", "").strip()
        except:
            return "No disponible"
    elif IS_LINUX:
        try:
            return subprocess.check_output(["sudo", "dmidecode", "-t", "baseboard"], encoding="utf-8").strip()
        except:
            return "No disponible"

print_save("\n[PLACA BASE]", SECTION)
print_save(get_motherboard())

# ========================= UPTIME =========================
def get_uptime():
    boot = psutil.boot_time()
    uptime_sec = int(datetime.now().timestamp() - boot)
    hours = uptime_sec // 3600
    minutes = (uptime_sec % 3600) // 60
    return f"{hours}h {minutes}m"

print_save("\n[TIEMPO DE ACTIVIDAD]", SECTION)
print_save(f"Uptime: {get_uptime()}")

# Pie de informe
print_save("\n" + "=" * 70, TITLE)
print_save(f"Informe generado con system_info_visual.py", TITLE)
print_save("=" * 70, TITLE)

f.close()
print(f"\n✅ Informe guardado en: {filename}")
