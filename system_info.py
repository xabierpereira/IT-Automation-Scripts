#!/usr/bin/env python3
"""
system_info.py - Generador de informes del sistema

Uso: python system_info.py
El informe se muestra en pantalla y se guarda automáticamente en un archivo.
Requisitos: pip install psutil
"""

import platform
import psutil
import socket
import getpass
import sys
import subprocess
from datetime import datetime

# ---------------------------------------
# Archivo de salida
# ---------------------------------------
filename = f"informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
f = open(filename, "w", encoding="utf-8")

def print_save(text=""):
    """Imprime en pantalla y guarda en archivo al mismo tiempo"""
    print(text)
    f.write(text + "\n")

# ---------------------------------------
# Función para ejecutar PowerShell
# ---------------------------------------
def run_powershell(cmd):
    try:
        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", cmd],
            encoding="utf-8",
            errors="ignore"
        )
        return output.strip()
    except:
        return "No disponible"

# ---------------------------------------
# Funciones GPU
# ---------------------------------------
def get_gpu_info():
    """
    Devuelve lista de diccionarios con GPUs y VRAM (>0 MB)
    """
    raw = run_powershell(
        "(Get-CimInstance Win32_VideoController | Select Name, AdapterRAM | Format-List | Out-String)"
    ).replace("\r", "").strip()

    gpus = []
    import re
    blocks = raw.split("\n\n")
    for block in blocks:
        name_match = re.search(r"Name\s*:\s*(.+)", block)
        ram_match = re.search(r"AdapterRAM\s*:\s*(\d+)", block)
        if name_match:
            name = name_match.group(1).strip()
            ram = int(ram_match.group(1)) if ram_match else 0
            if ram > 0:
                gpus.append({"name": name, "vram": f"{ram//(1024**2)} MB"})
    return gpus

# ---------------------------------------
# Funciones de red
# ---------------------------------------
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
    try:
        output = subprocess.check_output(
            ["netsh", "wlan", "show", "interfaces"],
            encoding="utf-8",
            errors="ignore"
        )
        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
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

# ---------------------------------------
# Función placa base
# ---------------------------------------
def get_motherboard():
    return run_powershell(
        "(Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product | Format-List | Out-String)"
    ).replace("\r", "").strip()

# ---------------------------------------
# Función uptime
# ---------------------------------------
def get_uptime():
    boot = psutil.boot_time()
    uptime_sec = int(datetime.now().timestamp() - boot)
    hours = uptime_sec // 3600
    minutes = (uptime_sec % 3600) // 60
    return f"{hours}h {minutes}m"

# ---------------------------------------
# GENERAR INFORME
# ---------------------------------------
print_save("=" * 60)
print_save(f"{'INFORME DE SISTEMA':^60}")
print_save(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^60}")
print_save("=" * 60)

# SISTEMA OPERATIVO
print_save("\n[SISTEMA OPERATIVO]")
print_save(f"OS: {platform.system()} {platform.release()}")
print_save(f"Versión: {platform.version()}")
print_save(f"Arquitectura: {platform.machine()}")
print_save(f"Hostname: {socket.gethostname()}")
print_save(f"Usuario: {getpass.getuser()}")
print_save(f"Python: {sys.version.split()[0]}")

# CPU
print_save("\n[PROCESADOR]")
cpu_model = run_powershell("(Get-CimInstance Win32_Processor).Name")
print_save(f"Procesador: {cpu_model}")
print_save(f"Núcleos físicos: {psutil.cpu_count(logical=False)}")
print_save(f"Núcleos lógicos: {psutil.cpu_count(logical=True)}")
print_save(f"Uso CPU: {psutil.cpu_percent(interval=1)}%")

# GPU
gpu_list = get_gpu_info()
print_save("\n[GRÁFICOS]")
for gpu in gpu_list:
    print_save(f"{gpu['name']}: {gpu['vram']}")

# RAM
print_save("\n[MEMORIA RAM]")
ram = psutil.virtual_memory()
print_save(f"Total: {ram.total / (1024**3):.2f} GB")
print_save(f"Disponible: {ram.available / (1024**3):.2f} GB")
print_save(f"Usado: {ram.percent}%")

# DISCO
print_save("\n[ALMACENAMIENTO]")
for partition in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(partition.mountpoint)
        print_save(f"\n{partition.device} ({partition.fstype})")
        print_save(f"  Total: {usage.total / (1024**3):.2f} GB")
        print_save(f"  Usado: {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
        print_save(f"  Libre: {usage.free / (1024**3):.2f} GB")
    except:
        pass

# Tipo de disco físico
disk_types = run_powershell("Get-PhysicalDisk | Select FriendlyName, MediaType | Format-Table -HideTableHeaders | Out-String").strip()
print_save(disk_types)

# RED
print_save("\n[RED]")
print_save(f"Adaptador activo: {get_active_network_adapter()}")
print_save(f"IP Local: {get_local_ip()}")
print_save(f"Red (SSID): {get_wifi_name()}")
print_save(f"Velocidad del enlace: {get_network_speed()}")

# BATERÍA
battery = psutil.sensors_battery()
if battery:
    print_save("\n[BATERÍA]")
    print_save(f"Nivel: {battery.percent}%")
    print_save(f"Enchufado: {'Sí' if battery.power_plugged else 'No'}")

# PLACA BASE
print_save("\n[PLACA BASE]")
print_save(get_motherboard())

# TIEMPO DE ACTIVIDAD
print_save("\n[TIEMPO DE ACTIVIDAD]")
print_save(f"Uptime: {get_uptime()}")

# FIN
print_save("\n" + "=" * 60)
print_save("Informe generado con system_info.py")
print_save("=" * 60)
print_save(f"\n✅ Informe guardado en: {filename}")



f.close()
