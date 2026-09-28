# Guía Institucional: Publicación en GitHub Pages y Ruta hacia Google for Nonprofits — IBPSA Perú
**Versión**: 1.0.0  
**Entidad**: IBPSA Perú  
**Correo actual puente**: `ibpsaperu2026@gmail.com`  
**Dominio institucional futuro**: `@ibpsaperu.com` (o `@ibpsa.pe`)  
**Costo total de infraestructura**: **$0.00 USD de por vida**

---

## 1. Arquitectura Digital para IBPSA Perú

Esta arquitectura es el estándar utilizado por instituciones científicas internacionales (como IBPSA Internacional, ASHRAE y universidades):

```text
                                DOMINIO: ibpsaperu.com
                                          │
            ┌─────────────────────────────┴─────────────────────────────┐
            ▼                                                           ▼
    REGISTROS MX (Correo)                                      REGISTROS CNAME (Web)
            │                                                           │
            ▼                                                           ▼
  GOOGLE FOR NONPROFITS                                        GITHUB PAGES
(Google Workspace Gratis)                                (Alojamiento Web Gratis)
• presidencia@ibpsaperu.com                              • clima.ibpsaperu.com
• contacto@ibpsaperu.com                                 • Visor interactivo 100% público
• Google Drive 30 GB+                                    • Cero caídas, CDN de Microsoft
• $10,000 USD/mes en Google Ads                          • Código abierto auditable
```

---

## 2. Paso a Paso: Publicar en GitHub Pages Hoy Mismo (Fase 1)

### Paso A: Crear la Cuenta u Organización en GitHub (2 minutos)
1. Entra a [github.com](https://github.com/) e inicia sesión (o regístrate con `ibpsaperu2026@gmail.com`).
2. Puedes usar el nombre de usuario **`ibpsaperu`** (o crear una Organización gratuita llamada `ibpsaperu`).
3. En la esquina superior derecha, haz clic en **"+" > "New repository"**.
4. Nombre del repositorio: **`auditoria-clima-peru`** (o `clima-peru`).
5. Selecciona la opción **Public** (Público, para que GitHub Pages sea 100% gratuito).
6. Deja desmarcadas las casillas de README o .gitignore (ya los tenemos listos en tu computadora).
7. Haz clic en **"Create repository"**.
8. Copia la URL que te muestra GitHub, que será algo como:  
   `https://github.com/ibpsaperu/auditoria-clima-peru.git`

---

### Paso B: Subir los Archivos con el Script Automático
En tu computadora ya hemos preparado todo (incluyendo el archivo `.gitignore` que excluye automáticamente los 11.5 GB de modelos temporales y deja solo los archivos esenciales y la web):

1. Haz doble clic en el archivo:
   ```text
   Scripts\publicar_github.bat
   ```
   *(O en PowerShell: `.\Scripts\publicar_github.ps1`)*.
2. El script inicializará el repositorio local de Git y te pedirá la URL que copiaste en el Paso A.
3. Pega la URL y presiona ENTER.
4. Si es la primera vez que usas Git con GitHub, se abrirá una ventana en tu navegador para que inicies sesión y autorices la subida.
5. En pocos segundos, todo tu código y la herramienta web quedarán respaldados en GitHub.

---

### Paso C: Activar GitHub Pages en 1 Clic
1. Entra a tu repositorio en GitHub (`https://github.com/ibpsaperu/auditoria-clima-peru`).
2. Ve a la pestaña **Settings** (Configuración en la barra superior).
3. En el menú de la izquierda, haz clic en **Pages**.
4. En la sección **Build and deployment > Source**, cambia la opción a:  
   👉 **`GitHub Actions`**.
5. ¡Listo! Como ya dejamos configurado el archivo `.github/workflows/deploy-pages.yml`, GitHub compilará y publicará de inmediato la carpeta `Final Results/web`.
6. En 30 segundos, tu página estará activa mundialmente en:  
   `https://ibpsaperu.github.io/auditoria-clima-peru/`

---

## 3. Conectar el Dominio Propio (Cuando adquieran `ibpsaperu.com`)

Cuando la asociación adquiera su dominio (ej. `ibpsaperu.com` o `ibpsa.pe`):

1. Entra a tu repositorio en GitHub > **Settings > Pages**.
2. En la casilla **Custom domain**, escribe el subdominio deseado:  
   `clima.ibpsaperu.com`
3. Haz clic en **Save**.
4. En el panel de control donde compraste el dominio (ej. Cloudflare, Namecheap o Punto.pe), agregas un registro DNS:
   * **Tipo**: `CNAME`
   * **Nombre**: `clima`
   * **Destino**: `ibpsaperu.github.io`
5. GitHub detectará el registro y activará automáticamente el certificado de seguridad **HTTPS (candado verde)** sin costo adicional.

---

## 4. Hoja de Ruta para Postular a Google for Nonprofits (Google para ONGs)

Para obtener cuentas de correo corporativas gratuitas con Google (`@ibpsaperu.com`) para la junta directiva y socios:

### Requisitos Legales en Perú:
1. **Personería Jurídica Vigente**: Estar inscrito en SUNARP como Asociación Civil sin fines de lucro (RUC 20 en SUNAT).
2. **Validación en TechSoup Perú**: Google valida a las ONGs de Perú a través del socio internacional **TechSoup / Percent**.
   - Ingresan a [TechSoup Perú](https://www.techsoup.global/es) y registran a IBPSA Perú con copia de la partida registral y ficha RUC.
   - En 3 a 7 días hábiles, TechSoup emite un **Token de Validación**.

### Activación de Beneficios de Google:
1. Con ese token, entran a [Google for Nonprofits](https://www.google.com/nonprofits/).
2. Inician sesión con la cuenta de Google institucional y solicitan la membresía.
3. Una vez aprobados (suele tardar 48 horas), acceden a los siguientes beneficios sin costo:
   * **Google Workspace for Nonprofits (Gratis para siempre)**: Hasta 2,000 cuentas de correo de Gmail con tu dominio `@ibpsaperu.com`, 30 GB de almacenamiento por usuario en Google Drive y Google Meet ilimitado.
   * **Google Ad Grants**: Hasta **$10,000 USD mensuales** de crédito gratuito en el motor de búsqueda de Google para promocionar eventos, cursos o la herramienta de clima de IBPSA Perú.
   * **Google Cloud**: Créditos adicionales para proyectos tecnológicos.

### Configuración del Correo en el Dominio:
En el panel del dominio `ibpsaperu.com`, se agregan los registros MX de Google Workspace. Esto no interfiere para nada con la web de GitHub Pages, permitiendo que ambos servicios convivan en perfecta armonía.
