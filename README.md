# 🤖 IT Automation Scripts

Colección de scripts Python para automatizar tareas comunes de soporte técnico IT.

## 🎯 Objetivo

Herramientas prácticas que ahorran tiempo en diagnóstico, limpieza y documentación de sistemas.

## 📜 Scripts Disponibles

### 1. 📊 `system_info.py` - Informe Completo del Sistema

Genera reporte detallado con toda la información del sistema.

**Uso:**
```bash
python system_info.py
python system_info.py > informe.txt  # Guardar en archivo
```

**Información incluida:**
- Sistema operativo y versión
- Hardware (CPU, RAM, disco)
- Red (IP, interfaces, estadísticas)
- Procesos top consumidores
- Temperaturas (si disponible)
- Batería (si aplica)

**Casos de uso:**
- Diagnóstico remoto (cliente envía informe)
- Documentación de equipos
- Troubleshooting inicial
- Auditoría de hardware

---

### 2. 🌐 `network_diagnostic.py` - Diagnóstico de Red

Test completo de conectividad de red paso a paso.

**Uso:**
```bash
python network_diagnostic.py
```

**Tests realizados:**
- ✅ Configuración IP local
- ✅ Conectividad gateway
- ✅ Conectividad internet (DNS públicos)
- ✅ Resolución DNS
- ✅ Puertos comunes (HTTP, HTTPS, DNS)
- ✅ Medición latencia

**Salida:** Diagnóstico claro con estado OK/FAIL y sugerencias de solución

**Casos de uso:**
- "No tengo internet" → Este script identifica dónde falla
- Diagnóstico remoto guiado
- Documentar problemas de red
- Training de juniors

---

### 3. 🧹 `cleanup_temp.py` - Limpieza Archivos Temporales

Limpia archivos temporales de Windows para liberar espacio.

**Uso:**
```bash
# Simular (ver qué se borraría)
python cleanup_temp.py --dry-run

# Ejecutar limpieza real
python cleanup_temp.py
```

⚠️ **Ejecutar como Administrador en Windows**

**Directorios limpiados:**
- `%TEMP%` (usuario)
- `C:\Windows\Temp`
- Windows Update cache
- Prefetch
- Thumbnails cache

**Seguridad:**
- Modo simulación disponible
- Confirmación antes de borrar
- Manejo de errores de permisos
- Informe detallado de espacio liberado

**Casos de uso:**
- PC con poco espacio en disco
- Mantenimiento preventivo
- Antes de actualizaciones grandes
- Troubleshooting problemas disco lleno

---

### 4. 📋 `installed_programs.py` - Lista Programas Instalados

Lista todos los programas instalados en Windows con detalles.

**Uso:**
```bash
python installed_programs.py
python installed_programs.py > programas.txt  # Exportar
```

**Información mostrada:**
- Nombre del programa
- Versión
- Editor/Fabricante
- Fecha instalación (si disponible)

**Estadísticas adicionales:**
- Total de programas
- Top editores
- Programas sin versión

**Casos de uso:**
- Auditoría de software
- Documentación pre-formateo
- Identificar software a desinstalar
- Comparar equipos
- Inventario IT

---

## 🔧 Requisitos

### Python 3.6+

```bash
python --version  # Verificar versión
```

### Librería `psutil`

```bash
pip install psutil
```

O con requirements:
```bash
pip install -r requirements.txt
```

---

## 📥 Instalación

### Opción 1: Clonar repositorio
```bash
git clone https://github.com/xabierpereira/IT-Automation-Scripts.git
cd IT-Automation-Scripts
pip install -r requirements.txt
```

### Opción 2: Descargar scripts individuales
Descarga solo el script que necesites y ejecuta:
```bash
pip install psutil
python script_name.py
```

---

## 💡 Casos de Uso Reales

### Escenario 1: Cliente reporta "Internet lento"
```bash
1. python system_info.py > cliente_sistema.txt
2. python network_diagnostic.py
   → Identifica: DNS lento
3. Cambiar DNS a 8.8.8.8
```

### Escenario 2: PC muy lento
```bash
1. python system_info.py
   → Verifica: Disco al 100%, RAM al 95%
2. python cleanup_temp.py
   → Libera: 5GB
3. python installed_programs.py
   → Identifica: 50+ programas basura
```

### Escenario 3: Auditoría remota
```bash
# Enviar al cliente por email:
1. system_info.py
2. installed_programs.py

# Cliente ejecuta y envía .txt
# Técnico analiza sin acceso remoto
```

---

## 🎓 Para Técnicos Junior

**Ventajas de usar scripts:**
- ✅ Metodología sistemática
- ✅ No olvidas pasos
- ✅ Resultados documentados
- ✅ Apredes troubleshooting estructurado

**Cómo aprovecharlos:**
1. Ejecuta los scripts para entender qué verifican
2. Lee el código para aprender los comandos
3. Modifica según tus necesidades
4. Comparte con tu equipo

---

## 🔜 Próximos Scripts (roadmap)

- [ ] `wifi_scanner.py` - Escanear redes WiFi cercanas
- [ ] `driver_updater.py` - Verificar drivers desactualizados
- [ ] `startup_optimizer.py` - Gestión programas de inicio
- [ ] `backup_documents.py` - Backup automático carpetas importantes
- [ ] `malware_scanner.py` - Scan básico de procesos sospechosos

---

## 🤝 Contribuciones

Pull requests bienvenidos. Para cambios mayores, abre un issue primero.

**Ideas para contribuir:**
- Añadir scripts nuevos
- Mejorar scripts existentes
- Traducir a otros idiomas
- Añadir soporte Linux/macOS
- Mejorar documentación

---

## ⚠️ Disclaimer

Estos scripts son herramientas de diagnóstico y limpieza. Usar bajo tu propio riesgo.

**Recomendaciones:**
- Siempre haz backup antes de limpiezas
- Lee el código antes de ejecutar
- Ejecuta en entorno de prueba primero
- No uses en sistemas críticos sin verificar

---

## 📞 Soporte

¿Encontraste un bug? ¿Tienes sugerencias?

- 🐛 Issues: [github.com/xabierpereira/IT-Automation-Scripts/issues](https://github.com/xabierpereira/IT-Automation-Scripts/issues)
- 💬 Discussions: Pestaña Discussions en GitHub
- 📧 Email: xabierpereira40@gmail.com

---

## 👨‍💻 Autor

**Xabier Pereira**  
Técnico IT Junior | IFCT0309  

📧 xabierpereira40@gmail.com  
💼 [LinkedIn](https://linkedin.com/in/xabierpereira)  
💻 [GitHub](https://github.com/xabierpereira)  

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

Uso libre para aprendizaje, trabajo personal y comercial.

---

## ⭐ Agradecimientos

Si estos scripts te ayudaron, considera:
- ⭐ Dar star al repositorio
- 🔄 Compartir con otros técnicos IT
- 💬 Dejar feedback en Issues/Discussions
- 🤝 Contribuir con mejoras

---

![Visitor Count](https://komarev.com/ghpvc/?username=xabierpereira&color=blue&label=Visitas)

**Última actualización:** Febrero 2026
