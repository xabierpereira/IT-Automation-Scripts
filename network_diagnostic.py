#!/usr/bin/env python3
"""
Network Diagnostic Tool (v2.0)
Diagnóstico completo de conectividad de red mejorado para Windows/Linux

Autor: Xabier Pereira
"""

import socket
import subprocess
import platform
import time
from datetime import datetime

def print_header(title):
    """Imprime cabecera de sección"""
    print("\n" + "=" * 60)
    print(f"   {title}")
    print("=" * 60)

def get_real_ip():
    """Obtiene la IP real de la interfaz activa (evita 127.0.1.1 en Linux)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No requiere conexión real, solo detecta por dónde saldría el tráfico
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except:
            ip = "No detectada"
    finally:
        s.close()
    return ip

def run_command(command):
    """Ejecuta comando y devuelve output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout
    except Exception:
        return ""

def test_ping(host, name=""):
    """Test ping a un host"""
    is_win = platform.system().lower() == 'windows'
    param = '-n' if is_win else '-c'
    command = f'ping {param} 4 {host}'
    
    print(f"\n🔍 Testing {name or host}...")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"   ✅ {name or host} - RESPONDE")
            # Extraer tiempo de la última línea de respuesta exitosa
            lines = [l for l in result.stdout.split('\n') if 'time=' in l.lower() or 'tiempo=' in l.lower()]
            if lines:
                print(f"      {lines[-1].strip()}")
            return True
        else:
            print(f"   ❌ {name or host} - NO RESPONDE")
            return False
    except:
        return False

def test_dns(domain):
    """Test resolución DNS"""
    print(f"\n🔍 Resolviendo DNS: {domain}")
    try:
        ip = socket.gethostbyname(domain)
        print(f"   ✅ {domain} → {ip}")
        return True, ip
    except:
        print(f"   ❌ No se pudo resolver {domain}")
        return False, None

def test_port(host, port, service_name=""):
    """Test si un puerto está abierto"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    try:
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"   ✅ Puerto {port} ({service_name}) ABIERTO")
            return True
        else:
            print(f"   ❌ Puerto {port} ({service_name}) CERRADO/BLOQUEADO")
            return False
    except:
        return False
    finally:
        sock.close()

def main():
    is_windows = platform.system().lower() == 'windows'
    
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 20 + "DIAGNÓSTICO DE RED" + " " * 20 + "║")
    print("╚" + "═" * 58 + "╝")
    print(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # ========== INFORMACIÓN LOCAL ==========
    print_header("INFORMACIÓN LOCAL")
    
    print(f"📌 Hostname: {socket.gethostname()}")
    print(f"📌 IP Local Detectada: {get_real_ip()}")
    
    if is_windows:
        print("\n📋 Resumen Adaptadores (Windows):")
        output = run_command('ipconfig')
        for line in output.split('\n'):
            if any(k in line.lower() for k in ['ipv4', 'puerta', 'gateway', 'adaptador']):
                if ":" in line: print(f"   {line.strip()}")
    else:
        print("\n📋 Resumen Adaptadores (Linux):")
        output = run_command("ip -4 addr show scope global | grep inet")
        if output:
            for line in output.split('\n'):
                if line: print(f"   {line.strip()}")

    # ========== TEST CONECTIVIDAD LOCAL ==========
    print_header("TEST 1: CONECTIVIDAD LOCAL")
    test_ping('127.0.0.1', 'Loopback (Interno)')
    
    gateway = None
    if is_windows:
        output = run_command('ipconfig')
        for line in output.split('\n'):
            if 'puerta de enlace' in line.lower() or 'default gateway' in line.lower():
                parts = line.split(':')
                if len(parts) > 1 and parts[1].strip():
                    gateway = parts[1].strip()
                    break
    else:
        output = run_command("ip route | grep default")
        if output:
            parts = output.split()
            if len(parts) > 2: gateway = parts[2]

    if gateway:
        print(f"\n📍 Gateway detectado: {gateway}")
        test_ping(gateway, f'Gateway ({gateway})')
    else:
        print("\n⚠️ No se detectó Gateway automáticamente.")

    # ========== TEST INTERNET Y DNS ==========
    print_header("TEST 2: INTERNET Y DNS")
    
    internet_ok = test_ping('8.8.8.8', 'Google DNS')
    dns_ok, _ = test_dns('google.com')

    # ========== TEST PUERTOS ==========
    print_header("TEST 3: PUERTOS CRÍTICOS")
    test_port('google.com', 443, 'HTTPS')
    test_port('8.8.8.8', 53, 'DNS')

    # ========== LATENCIA DETALLADA ==========
    print_header("TEST 4: ESTADÍSTICAS DE LATENCIA")
    targets = [('8.8.8.8', 'Google'), ('1.1.1.1', 'Cloudflare')]
    for ip, name in targets:
        print(f"\n📡 {name}:")
        param = '-n' if is_windows else '-c'
        output = run_command(f'ping {param} 5 {ip}')
        for line in output.split('\n'):
            if any(k in line.lower() for k in ['average', 'media', 'min', 'max']):
                print(f"   {line.strip()}")

    # ========== RESUMEN ==========
    print_header("RESULTADO FINAL")
    puntos = 0
    if gateway: puntos += 1
    if internet_ok: puntos += 1
    if dns_ok: puntos += 1

    status = "🔴 SIN CONEXIÓN"
    if puntos == 3: status = "🟢 TODO OK"
    elif puntos == 2: status = "🟡 PROBLEMA PARCIAL (Revisar DNS)"
    
    print(f"Estado General: {status}")
    print(f"Puntuación: {puntos}/3 tests principales superados.")
    
    print("\n" + "=" * 60)
    print("Autor: Xabier Pereira | github.com/xabierpereira")
    print("=" * 60)

if __name__ == "__main__":
    main()