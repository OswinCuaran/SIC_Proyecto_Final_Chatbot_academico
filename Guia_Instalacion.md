# Guía de Instalación
## Chatbot Académico - UNAL Manizales

### Integrantes
- Oswin Olsman Cuaran
- Edwin Hernan Chenas
- Santiago Felipe Quitiaquez

---

## Requisitos Previos

| Herramienta | Versión mínima | Descarga |
|-------------|---------------|----------|
| Python | 3.11 o superior | https://www.python.org |
| Git | Cualquier versión | https://git-scm.com |
| Navegador web | Chrome, Firefox, Edge | - |

---

## 1. Clonar el Repositorio

```bash
git clone https://github.com/OswinCuaran/SIC_Proyecto_Final_Chatbot_academico.git
cd SIC_Proyecto_Final_Chatbot_academico
```

---

## 2. Configurar el Backend

### 2.1 Crear entorno virtual
```bash
cd backend
python -m venv venv
```

### 2.2 Activar entorno virtual

**Windows (CMD):**
```bash
venv\Scripts\activate
```

**Windows (Git Bash) / Linux / Mac:**
```bash
source venv/bin/activate
```

### 2.3 Instalar dependencias
```bash
pip install --timeout 300 -r requirements.txt
```

> Este proceso puede tardar varios minutos ya que descarga PyTorch y otros modelos de IA.

---

## 3. Configurar Variables de Entorno

Crea un archivo llamado `.env` dentro de la carpeta `backend/` con el siguiente contenido:

OPENROUTER_API_KEY=tu_api_key_aqui
OPENROUTER_MODEL=openai/gpt-3.5-turbo

> 📌 Para obtener una API key gratuita ve a https://openrouter.ai y crea una cuenta.

---

## 4. Ejecutar el Sistema

Desde la carpeta `backend/` con el entorno virtual activado:

```bash
python run.py
```

El sistema realizará automáticamente los siguientes pasos:
1. Cargará los documentos académicos en la base de datos vectorial
2. Generará los embeddings de todos los documentos
3. Iniciará el servidor web

> La primera ejecución puede tardar entre 5 y 10 minutos mientras descarga el modelo de embeddings y procesa los documentos.

---

## 5. Acceder al Chatbot

Una vez que aparezca el mensaje:

Base de conocimiento cargada exitosamente
 Iniciando servidor...
 URL: http://localhost:8000
 Abre tu navegador y ve a:
 http://localhost:8000

---

## 6. Verificar que funciona

En el navegador deberías ver:
- La interfaz del chatbot con diseño ciberpunk
- El badge **"Sistema activo · 459 docs"** en la esquina superior derecha
- Las sugerencias de preguntas en el centro

Prueba haciendo una pregunta como:
- *¿Qué materias hay en el semestre 3?*
- *¿Cuáles son los prerrequisitos de Bases de Datos I?*

---

## 7. Detener el Sistema

Para detener el servidor presiona:
- **Ctrl + C** en la terminal donde se ejecuta `python run.py`

---

## 8. Solución de Problemas Comunes

**Error: timeout al instalar dependencias**
```bash
pip install --timeout 300 --retries 5 -r requirements.txt
```

**La base de datos no carga**
```bash
# Ejecutar el cargador manualmente
python cargar_chroma.py
```

---

## 9. Estructura del Proyecto

SIC_Proyecto_Final_Chatbot_academico/
├── backend/
│   ├── app/
│   │   ├── init.py
│   │   ├── main.py          # Servidor Flask y rutas API
│   │   └── rag.py           # Motor de búsqueda semántica
│   ├── data/
│   │   ├── malla_curricular.json
│   │   ├── asignaturas.csv
│   │   └── Contenido_asignaturas.pdf
│   ├── chroma_db/           # Base de datos vectorial (se genera automáticamente)
│   ├── cargar_chroma.py     # Carga documentos en ChromaDB
│   ├── run.py               # Punto de entrada del sistema
│   ├── requirements.txt     # Dependencias de Python
│   └── .env                 # Variables de entorno (crear manualmente)
├── frontend/
│   ├── index.html           # Interfaz principal
│   ├── css/
│   │   └── style.css        # Estilos ciberpunk
│   └── js/
│       └── app.js           # Lógica del frontend
├── ANALISIS_DISEÑO.md       # Documento de análisis y diseño
├── GUIA_INSTALACION.md      # Este archivo
├── .gitignore
└── README.md

---

*Universidad Nacional de Colombia - Sede Manizales*
*Programa: Administración de Sistemas Informáticos*
*Materia: Sistemas Inteligentes Computacionales*