from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
from .rag import buscar_contexto, obtener_estado_coleccion

# Cargar variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

def consultar_llm(pregunta, contexto):
    """Envía la pregunta y contexto al LLM via OpenRouter"""
    
    prompt_sistema = """Eres un asistente académico virtual de la Universidad Nacional de Colombia, 
sede Manizales, para el programa de Administración de Sistemas Informáticos.

Tu función es responder preguntas sobre:
- Materias y asignaturas del programa
- Contenidos y descripciones de cada materia
- Prerrequisitos de las materias
- Semestres y créditos
- Malla curricular

Usa únicamente la información del contexto proporcionado para responder.
Si no encuentras la información en el contexto, dilo amablemente.
Responde siempre en español de forma clara y organizada."""

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

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal del chatbot"""
    datos = request.get_json()
    
    if not datos or 'pregunta' not in datos:
        return jsonify({'error': 'Se requiere una pregunta'}), 400
    
    pregunta = datos['pregunta'].strip()
    
    if not pregunta:
        return jsonify({'error': 'La pregunta no puede estar vacía'}), 400
    
    # Buscar contexto relevante
    contexto = buscar_contexto(pregunta)
    
    # Consultar al LLM
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

@app.route('/', methods=['GET'])
def inicio():
    return jsonify({'mensaje': 'Chatbot Académico UNAL - API activa'})

if __name__ == '__main__':
    app.run(debug=True, port=8000)