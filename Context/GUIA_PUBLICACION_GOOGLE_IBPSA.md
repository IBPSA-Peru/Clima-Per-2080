# Guía de Publicación en Google Firebase Hosting — IBPSA Perú
**Versión**: 1.0.0  
**Entidad**: IBPSA Perú  
**Cuenta de Google institucional**: `ibpsaperu2026@gmail.com`  
**Costo mensual de infraestructura**: **$0.00 USD (Plan Spark Gratuito de Google)**

---

## 1. ¿Por qué Google Firebase Hosting para IBPSA Perú?

Para una asociación científica y técnica sin fines de lucro como **IBPSA Perú**, Firebase Hosting de Google ofrece ventajas decisivas:

1. **Costo Cero Real ($0.00)**:
   - 10 GB de almacenamiento gratuito (el visor completo pesa apenas 1 MB).
   - 360 MB de transferencia de datos diaria (~10 GB/mes), suficiente para miles de visitas al mes.
   - No requiere ingresar tarjeta de crédito para el plan gratuito Spark.
2. **Infraestructura y Seguridad de Google**:
   - Alojado en la red global de servidores CDN de Google (carga ultra rápida desde Lima o cualquier lugar del mundo en menos de 200 ms).
   - Certificado de seguridad **SSL (HTTPS)** automático, oficial y renovado de por vida por Google sin costo.
3. **Dominio Público Inmediato**:
   - Google te asigna de inmediato dos direcciones web gratuitas:
     - `https://ibpsa-clima-peru.web.app`
     - `https://ibpsa-clima-peru.firebaseapp.com`
4. **Conexión a Dominio Propio en el Futuro**:
   - Cuando IBPSA adquiera su dominio (ej. `ibpsa.pe` o `clima.ibpsa.pe`), se enlaza en 2 clics desde la consola de Google sin pagar nada extra.

---

## 2. Paso a Paso: Despliegue en 3 Minutos

### Paso A: Registrar el Proyecto en la Consola de Google (Solo la primera vez)

1. Abre tu navegador e ingresa a [Firebase Console](https://console.firebase.google.com/) con la cuenta `ibpsaperu2026@gmail.com`.
2. Haz clic en **"Crear un proyecto"** (o "Agregar proyecto").
3. Escribe el nombre del proyecto: `ibpsa-clima-peru` (o el nombre que prefieras).
4. Google te preguntará si deseas habilitar Google Analytics (es opcional y gratuito, útil si quieres saber cuántos visitantes entran al mes).
5. Haz clic en **"Crear proyecto"**. En 10 segundos el proyecto estará creado en los servidores de Google.

---

### Paso B: Publicar la Herramienta con 1 Solo Clic

En esta carpeta de trabajo ya hemos dejado todo configurado (`firebase.json`, `.firebaserc` y scripts automáticos):

1. Haz doble clic en el archivo:
   ```text
   Scripts\desplegar_firebase.bat
   ```
   *(O si usas PowerShell: `.\Scripts\desplegar_firebase.ps1`)*.
2. El script detectará tu instalación de Node.js y abrirá automáticamente una ventana del navegador de Google para que inicies sesión con `ibpsaperu2026@gmail.com` y autorices la subida.
3. El script subirá los archivos a la nube de Google.
4. **¡Listo!** El script te mostrará la URL pública activa en internet para compartir con IBPSA y el público general.

---

## 3. Arquitectura de Cómputo Climático: Preguntas Frecuentes

### ¿Se necesita mantener una computadora o servidor encendido en línea?
**No.** La herramienta actual es una **aplicación web estática y autocontenida**.
- Todos los datos de las 8 ciudades, 4 horizontes temporales (Hoy, 2030, 2050, 2080) y 2 escenarios IPCC ya fueron procesados y empaquetados en un archivo optimizado de datos.
- Cuando un usuario ingresa a la web, su propio navegador (en su laptop, tablet o celular) dibuja los gráficos interactivos, mueve el dial solar y anima la nube psicrométrica.
- Los servidores de Google solo entregan el archivo. Por eso, el costo mensual de servidores para IBPSA es **$0.00**.

### ¿Cómo se actualizan los archivos EPW si hay nuevos datos en el futuro?
El flujo es local y limpio (Pipeline reproducible):
1. Descargas o agregas los nuevos EPWs en la carpeta `Data/`.
2. Ejecutas los scripts de preparación:
   ```powershell
   python Scripts/preparar_payload.py
   python Scripts/generar_visor.py
   ```
3. Ejecutas nuevamente:
   ```text
   Scripts\desplegar_firebase.bat
   ```
4. En menos de 30 segundos la web en internet se actualiza para todo el mundo.

### ¿Cómo permitir que los usuarios suban sus propios EPWs gratis (Fase 2)?
Si en el futuro deseas que cualquier usuario pueda arrastrar su propio archivo EPW para auditarlo en vivo:
- **Solución Recomendada (Client-Side / En el Navegador del Usuario)**:
  - Un archivo EPW tiene 8,760 filas de texto (~1.5 MB). Los navegadores modernos pueden leerlo y procesar sus estadísticas con JavaScript en ~200 milisegundos.
  - **Ventaja**: Cero servidores que pagar para IBPSA, escalabilidad infinita (no importa si entran 10 o 100,000 personas a la vez) y confidencialidad total (los usuarios no envían sus archivos a servidores externos, todo ocurre en su propia máquina).

---

## 4. Vincular el Dominio Propio de IBPSA (Cuando lo adquieran)

1. En [Firebase Console](https://console.firebase.google.com/), entra a tu proyecto `ibpsa-clima-peru`.
2. En el menú izquierdo ve a **Compilación > Hosting**.
3. Haz clic en el botón **"Agregar dominio personalizado"**.
4. Escribe el dominio deseado (ejemplo: `clima.ibpsa.pe` o `auditoria.ibpsaperu.org`).
5. Firebase te mostrará 1 o 2 registros DNS (Tipo TXT y CNAME / A) para verificar que eres el propietario.
6. Copias esos registros en el panel donde hayas comprado el dominio (ej. Nic.pe o Cloudflare).
7. En pocas horas, Google validará el dominio y le activará el candado de seguridad HTTPS de forma totalmente gratuita y automática.
