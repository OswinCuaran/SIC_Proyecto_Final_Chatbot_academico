import os
import json
import csv
import chromadb
from sentence_transformers import SentenceTransformer
import pdfplumber

# Inicializar modelo y ChromaDB
print("Iniciando carga de documentos...")
modelo = SentenceTransformer('all-MiniLM-L6-v2')

CHROMA_PATH = os.path.join(os.path.dirname(__file__), 'chroma_db')
cliente = chromadb.PersistentClient(path=CHROMA_PATH)

# Limpiar colección anterior si existe
try:
    cliente.delete_collection("academico_unal")
    print("Colección anterior eliminada")
except:
    pass

coleccion = cliente.create_collection(
    name="academico_unal",
    metadata={"hnsw:space": "cosine"}
)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
documentos = []
ids = []
contador = 0

# Cargar JSON - Malla curricular
print("Cargando malla curricular JSON...")
ruta_json = os.path.join(DATA_PATH, 'malla_curricular.json')
with open(ruta_json, 'r', encoding='utf-8') as f:
    malla = json.load(f)

for materia in malla:
    texto = f"""Materia: {materia['nombre']}
Código: {materia['codigo']}
Semestre: {materia.get('semestre', 'Optativa')}
Créditos: {materia['creditos']}
Tipología: {materia['tipologia']}
Prerrequisitos: {', '.join(materia['prerequisitos']) if materia['prerequisitos'] else 'Ninguno'}"""
    
    documentos.append(texto)
    ids.append(f"json_{contador}")
    contador += 1

print(f"  {contador} materias cargadas del JSON")

# Cargar CSV - Asignaturas
print("Cargando asignaturas CSV...")
ruta_csv = os.path.join(DATA_PATH, 'asignaturas.csv')
contador_csv = 0
with open(ruta_csv, 'r', encoding='latin-1') as f:
    lector = csv.DictReader(f)
    for fila in lector:
        texto = ', '.join([f"{k}: {v}" for k, v in fila.items() if v])
        documentos.append(texto)
        ids.append(f"csv_{contador}")
        contador += 1
        contador_csv += 1

print(f"  {contador_csv} filas cargadas del CSV")

# Cargar PDF - Contenido de asignaturas
print("Cargando contenido de asignaturas PDF...")
ruta_pdf = os.path.join(DATA_PATH, 'Contenido_asignaturas.pdf')
contador_pdf = 0
with pdfplumber.open(ruta_pdf) as pdf:
    for num_pagina, pagina in enumerate(pdf.pages):
        texto = pagina.extract_text()
        if texto and texto.strip():
            # Dividir en fragmentos de 500 caracteres
            fragmentos = [texto[i:i+500] for i in range(0, len(texto), 500)]
            for fragmento in fragmentos:
                if fragmento.strip():
                    documentos.append(fragmento)
                    ids.append(f"pdf_{contador}")
                    contador += 1
                    contador_pdf += 1

print(f"  {contador_pdf} fragmentos cargados del PDF")

# Generar embeddings y guardar en ChromaDB
print(f"\nGenerando embeddings para {len(documentos)} documentos...")
print("Esto puede tardar unos minutos...")

LOTE = 50
for i in range(0, len(documentos), LOTE):
    lote_docs = documentos[i:i+LOTE]
    lote_ids = ids[i:i+LOTE]
    embeddings = modelo.encode(lote_docs).tolist()
    
    coleccion.add(
        documents=lote_docs,
        embeddings=embeddings,
        ids=lote_ids
    )
    print(f"  Procesados {min(i+LOTE, len(documentos))}/{len(documentos)} documentos")

print(f"\nCarga completada exitosamente")
print(f"Total documentos en ChromaDB: {coleccion.count()}")