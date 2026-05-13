# Documento de Análisis y Diseño
## Chatbot Académico - Universidad Nacional de Colombia
### Programa: Administración de Sistemas Informáticos - Sede Manizales
### Materia: Sistemas Inteligentes Computacionales

---

## 1. Descripción del Problema

Los estudiantes del programa de Administración de Sistemas Informáticos de la Universidad Nacional de Colombia, sede Manizales, frecuentemente necesitan consultar información académica como materias por semestre, prerrequisitos, contenidos de asignaturas y estructura de la malla curricular. Esta información está dispersa en documentos PDF, archivos CSV y JSON, lo que dificulta el acceso rápido y eficiente.

**Problema identificado:** No existe un sistema conversacional que permita a los estudiantes consultar de forma natural y rápida la información académica del programa.

**Solución propuesta:** Desarrollo de un ChatBot académico inteligente usando técnicas de NLP y LLM orientado específicamente al programa de Administración de Sistemas Informáticos, implementado con tecnología RAG (Retrieval-Augmented Generation).

---

## 2. Objetivos

### Objetivo General
Desarrollar un asistente virtual conversacional que permita a los estudiantes consultar información académica del programa de Administración de Sistemas Informáticos de la UNAL Manizales de forma natural e intuitiva.

### Objetivos Específicos
- Implementar un sistema RAG que combine búsqueda semántica con generación de respuestas mediante LLM.
- Procesar y estructurar la información académica del programa en una base de datos vectorial.
- Desarrollar una interfaz web accesible e intuitiva para la interacción con el chatbot.
- Garantizar respuestas precisas y contextualizadas sobre el programa académico.

---

## 3. Técnica de Inteligencia Artificial Utilizada

### RAG (Retrieval-Augmented Generation)
El sistema utiliza la técnica RAG que combina dos componentes principales:

**3.1 Recuperación de Información (Retrieval)**
- Se procesan los documentos académicos y se convierten en vectores numéricos mediante embeddings.
- Modelo de embeddings: `all-MiniLM-L6-v2` de Sentence Transformers.
- Base de datos vectorial: ChromaDB con similitud coseno.
- Cuando el usuario hace una pregunta, se buscan los fragmentos más relevantes.

**3.2 Generación de Respuestas (Generation)**
- Los fragmentos relevantes se envían como contexto al LLM.
- Modelo LLM: `openai/gpt-3.5-turbo` via OpenRouter API.
- El LLM genera una respuesta coherente basada únicamente en el contexto recuperado.

### Ventajas del enfoque RAG
- Respuestas basadas en información real y actualizada del programa.
- Reduce las alucinaciones del LLM al anclar las respuestas en documentos reales.
- Fácil actualización de la base de conocimiento sin reentrenar el modelo.

---

## 4. Arquitectura del Sistema

┌─────────────────────────────────────────────────────┐
│                    USUARIO                          │
│              (Navegador Web)                        │
└─────────────────────┬───────────────────────────────┘
│ HTTP Request
▼
┌─────────────────────────────────────────────────────┐
│                  FRONTEND                           │
│         HTML + CSS + JavaScript                     │
│    (Interfaz conversacional estilo ciberpunk)       │
└─────────────────────┬───────────────────────────────┘
│ POST /api/chat
▼
┌─────────────────────────────────────────────────────┐
│                  BACKEND (Flask)                    │
│                                                     │
│  ┌──────────────┐      ┌────────────────────────┐   │
│  │   RAG Engine │      │    OpenRouter API      │   │
│  │              │      │   (GPT-3.5-turbo)      │   │
│  │  ChromaDB    │────▶│                        │   │
│  │  Embeddings  │      │  Generación respuesta  │   │
│  └──────────────┘      └────────────────────────┘   │
└─────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│              BASE DE CONOCIMIENTO                   │
│                                                     │
│  malla_curricular.json  │  asignaturas.csv          │
│  Contenido_asignaturas.pdf                          │
│                                                     │
│  Total: 459 documentos vectorizados                 │
└─────────────────────────────────────────────────────┘

---

## 5. Tecnologías Utilizadas

| Componente | Tecnología 
|------------|-----------
| Backend | Python + Flask 
| Base de datos vectorial | ChromaDB 
| Embeddings | Sentence Transformers 
| Modelo de embeddings | all-MiniLM-L6-v2 
| LLM | GPT-3.5-turbo (OpenRouter) 
| Frontend | HTML + CSS + JavaScript 
| Control de versiones | Git + GitHub 
| Sistema operativo desarrollo | Debian (WSL) 

---

## 6. Diseño del Sistema

### 6.1 Flujo de una Consulta

1. Usuario escribe pregunta en el frontend
2. JavaScript envía POST a /api/chat
3. Flask recibe la pregunta
4. RAG Engine detecta contexto (semestre, materia, etc.)
5. Se generan embeddings de la pregunta
6. ChromaDB busca los documentos más similares
7. Se construye el prompt con contexto + pregunta
8. Se envía a OpenRouter (GPT-3.5-turbo)
9. Se recibe la respuesta del LLM
10. Flask retorna la respuesta al frontend
11. JavaScript muestra la respuesta en el chat

### 6.2 Estructura del Proyecto

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
│   ├── chroma_db/           # Base de datos vectorial
│   ├── cargar_chroma.py     # Carga documentos en ChromaDB
│   ├── run.py               # Punto de entrada del sistema
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── ANALISIS_DISEÑO.md
├── GUIA_INSTALACION.md
├── .gitignore
└── README.md

### 6.3 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | / | Sirve el frontend |
| POST | /api/chat | Recibe pregunta y retorna respuesta |
| GET | /api/estado | Estado del sistema y documentos cargados |

---

## 7. Fuentes de Datos

| Archivo | Contenido | Formato |
|---------|-----------|---------|
| malla_curricular.json | 54 materias con código, semestre, créditos, tipología y prerrequisitos | JSON |
| asignaturas.csv | Información complementaria de asignaturas | CSV |
| Contenido_asignaturas.pdf | Descripciones detalladas y contenidos de cada materia | PDF |

---

## 8. Resultados Obtenidos

El sistema desarrollado permite:
- Consultar materias por semestre de forma completa y precisa.
- Obtener prerrequisitos de cualquier asignatura del programa.
- Conocer el contenido detallado de cada materia.
- Consultar créditos y tipología de las asignaturas.
- Rechazar preguntas fuera del contexto académico.
- Indicar cuando no tiene información disponible.

---

## 9. Conclusiones

El desarrollo del Chatbot Académico demuestra la aplicabilidad de las técnicas de Inteligencia Artificial, específicamente RAG, en contextos educativos reales. La combinación de búsqueda semántica con modelos de lenguaje de gran escala permite crear asistentes virtuales precisos y contextualizados sin necesidad de reentrenar modelos costosos.

El sistema representa una solución práctica al problema de acceso a información académica, mejorando la experiencia del estudiante y demostrando el potencial de los Sistemas Inteligentes Computacionales en la administración de información universitaria.

---

### Integrantes
- Oswin Olsman Cuaran
- Edwin Hernan Chenas
- Santiago Felipe Quitiaquez

*Desarrollado para la materia Sistemas Inteligentes Computacionales*
*Universidad Nacional de Colombia - Sede Manizales*
*Programa: Administración de Sistemas Informáticos*