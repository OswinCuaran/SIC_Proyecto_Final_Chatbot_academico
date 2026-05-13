from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
from .rag import buscar_contexto, obtener_estado_coleccion

# Cargar variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Ruta al frontend
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_PATH)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

def consultar_llm(pregunta, contexto):
    """Envía la pregunta y contexto al LLM via OpenRouter"""
    
    prompt_sistema = """Eres un asistente académico virtual de la Universidad Nacional de Colombia, 
sede Manizales, para el programa de Administración de Sistemas Informáticos.

REGLAS ESTRICTAS QUE DEBES SEGUIR:
1. Responde ÚNICAMENTE con información del contexto proporcionado.
2. Si la pregunta es sobre una materia específica, busca SOLO la información de ESA materia.
3. Si no encuentras información específica de la materia preguntada, di exactamente: "No encontré información específica sobre esa materia en mi base de datos."
4. NUNCA mezcles información de una materia con otra.
5. Si preguntan por horarios específicos de clases (días, horas exactas), responde que esa información no está disponible en tu base de datos y recomienda consultar SIA o la secretaría del programa.
6. Si preguntan por profesores específicos, responde que esa información no está disponible.
7. Responde siempre en español de forma clara y organizada.

Tu función es responder preguntas sobre:
- Materias y asignaturas del programa
- Contenidos y descripciones de cada materia
- Prerrequisitos de las materias
- Semestres y créditos
- Malla curricular"""

    prompt_usuario = f"""Contexto académico:
{contexto}

Pregunta del estudiante: {pregunta}"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }

    respuesta = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=body
    )

    if respuesta.status_code == 200:
        return respuesta.json()['choices'][0]['message']['content']
    else:
        return f"Error al consultar el modelo: {respuesta.status_code}"

# ============ RUTAS DEL FRONTEND ============
@app.route('/')
def inicio():
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/css/<path:archivo>')
def css(archivo):
    return send_from_directory(os.path.join(FRONTEND_PATH, 'css'), archivo)

@app.route('/js/<path:archivo>')
def js(archivo):
    return send_from_directory(os.path.join(FRONTEND_PATH, 'js'), archivo)

# ============ RUTAS DE LA API ============
@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal del chatbot"""
    datos = request.get_json()
    
    if not datos or 'pregunta' not in datos:
        return jsonify({'error': 'Se requiere una pregunta'}), 400
    
    pregunta = datos['pregunta'].strip()
    
    if not pregunta:
        return jsonify({'error': 'La pregunta no puede estar vacía'}), 400
    
    contexto = buscar_contexto(pregunta)
    respuesta = consultar_llm(pregunta, contexto)
    
    return jsonify({
        'respuesta': respuesta,
        'pregunta': pregunta
    })

@app.route('/api/estado', methods=['GET'])
def estado():
    """Endpoint para verificar el estado del sistema"""
    total_docs = obtener_estado_coleccion()
    return jsonify({
        'estado': 'activo',
        'documentos_cargados': total_docs,
        'modelo': OPENROUTER_MODEL
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)