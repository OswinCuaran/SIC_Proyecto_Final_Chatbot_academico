import chromadb
from sentence_transformers import SentenceTransformer
import os

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

def buscar_contexto(pregunta, n_resultados=5):
    """Busca los documentos más relevantes para la pregunta"""
    if coleccion.count() == 0:
        return "No hay documentos cargados en la base de datos."
    
    embedding_pregunta = modelo.encode(pregunta).tolist()
    
    resultados = coleccion.query(
        query_embeddings=[embedding_pregunta],
        n_results=n_resultados
    )
    
    contexto = ""
    for i, documento in enumerate(resultados['documents'][0]):
        contexto += f"--- Fragmento {i+1} ---\n{documento}\n\n"
    
    return contexto

def obtener_estado_coleccion():
    """Retorna cuántos documentos hay cargados"""
    return coleccion.count()