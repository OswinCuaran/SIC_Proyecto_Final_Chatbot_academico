import chromadb
from sentence_transformers import SentenceTransformer
import os
import re

# Inicializar el modelo de embeddings
modelo = SentenceTransformer('all-MiniLM-L6-v2')

# Ruta de la base de datos vectorial
CHROMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'chroma_db')

# Inicializar ChromaDB
cliente_chroma = chromadb.PersistentClient(path=CHROMA_PATH)

coleccion = cliente_chroma.get_or_create_collection(
    name="academico_unal",
    metadata={"hnsw:space": "cosine"}
)

def detectar_semestre(pregunta):
    """Detecta si la pregunta menciona un semestre específico"""
    patrones = [
        r'semestre\s*(\d+)',
        r'(\d+)[°º]\s*semestre',
        r'semestre\s*([uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez]+)'
    ]
    for patron in patrones:
        match = re.search(patron, pregunta.lower())
        if match:
            numero = match.group(1)
            conversion = {
                'uno': '1', 'dos': '2', 'tres': '3', 'cuatro': '4',
                'cinco': '5', 'seis': '6', 'siete': '7', 'ocho': '8',
                'nueve': '9', 'diez': '10'
            }
            return conversion.get(numero, numero)
    return None

def buscar_contexto(pregunta, n_resultados=20):
    """Busca los documentos más relevantes para la pregunta"""
    if coleccion.count() == 0:
        return "No hay documentos cargados en la base de datos."

    embedding_pregunta = modelo.encode(pregunta).tolist()
    semestre = detectar_semestre(pregunta)
    contexto = ""

    # Si detecta semestre específico
    if semestre:
        try:
            resultado_semestre = coleccion.query(
                query_embeddings=[embedding_pregunta],
                n_results=3,
                where={"$and": [{"tipo": {"$eq": "semestre"}}, {"semestre": {"$eq": semestre}}]}
            )
            if resultado_semestre['documents'][0]:
                contexto += "=== INFORMACIÓN COMPLETA DEL SEMESTRE ===\n"
                for doc in resultado_semestre['documents'][0]:
                    contexto += doc + "\n\n"
        except:
            pass

        try:
            resultado_materias = coleccion.query(
                query_embeddings=[embedding_pregunta],
                n_results=10,
                where={"$and": [{"tipo": {"$eq": "materia"}}, {"semestre": {"$eq": semestre}}]}
            )
            if resultado_materias['documents'][0]:
                contexto += "=== MATERIAS DEL SEMESTRE ===\n"
                for doc in resultado_materias['documents'][0]:
                    contexto += doc + "\n\n"
        except:
            pass

    # Buscar primero en JSON materias y semestres - más confiable
    try:
        resultado_json = coleccion.query(
            query_embeddings=[embedding_pregunta],
            n_results=10,
            where={"tipo": {"$in": ["materia", "semestre"]}}
        )
        if resultado_json['documents'][0]:
            contexto += "=== DATOS DE LA MALLA CURRICULAR ===\n"
            for doc in resultado_json['documents'][0]:
                contexto += doc + "\n\n"
    except:
        pass

    # Buscar en PDF solo para contenidos de materias
    try:
        resultado_pdf = coleccion.query(
            query_embeddings=[embedding_pregunta],
            n_results=5,
            where={"tipo": {"$eq": "pdf"}}
        )
        if resultado_pdf['documents'][0]:
            contexto += "=== CONTENIDO DETALLADO ===\n"
            for doc in resultado_pdf['documents'][0]:
                contexto += doc + "\n\n"
    except:
        pass

    return contexto

def obtener_estado_coleccion():
    """Retorna cuántos documentos hay cargados"""
    return coleccion.count()