import os
import json
import csv
import chromadb
from sentence_transformers import SentenceTransformer
import pdfplumber

print("Iniciando carga de documentos...")
modelo = SentenceTransformer('all-MiniLM-L6-v2')

CHROMA_PATH = os.path.join(os.path.dirname(__file__), 'chroma_db')
cliente = chromadb.PersistentClient(path=CHROMA_PATH)

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
metadatos = []
contador = 0

# Cargar JSON
print("Cargando malla curricular JSON...")
ruta_json = os.path.join(DATA_PATH, 'malla_curricular.json')
with open(ruta_json, 'r', encoding='utf-8') as f:
    malla = json.load(f)

# Crear un documento por semestre con TODAS sus materias
semestres = {}
for materia in malla:
    sem = materia.get('semestre')
    if sem not in semestres:
        semestres[sem] = []
    semestres[sem].append(materia)

for sem, materias in semestres.items():
    if sem is None:
        tipo = "optativa"
    else:
        tipo = f"semestre_{sem}"

    # Documento completo del semestre
    texto = f"Materias del semestre {sem}:\n"
    for m in materias:
        texto += f"""
- Materia: {m['nombre']}
  Código: {m['codigo']}
  Créditos: {m['creditos']}
  Tipología: {m['tipologia']}
  Prerrequisitos: {', '.join(m['prerequisitos']) if m['prerequisitos'] else 'Ninguno'}
"""
    documentos.append(texto)
    ids.append(f"semestre_{tipo}_{contador}")
    metadatos.append({"tipo": "semestre", "semestre": str(sem)})
    contador += 1

    # Documento individual por materia
    for m in materias:
        texto_materia = f"""Materia: {m['nombre']}
Código: {m['codigo']}
Semestre: {sem}
Créditos: {m['creditos']}
Tipología: {m['tipologia']}
Prerrequisitos: {', '.join(m['prerequisitos']) if m['prerequisitos'] else 'Ninguno'}"""

        documentos.append(texto_materia)
        ids.append(f"materia_{m['codigo']}_{contador}")
        metadatos.append({"tipo": "materia", "semestre": str(sem), "nombre": m['nombre']})
        contador += 1

print(f"  {contador} documentos generados del JSON")

# Cargar CSV
print("Cargando asignaturas CSV...")
ruta_csv = os.path.join(DATA_PATH, 'asignaturas.csv')
contador_csv = 0
with open(ruta_csv, 'r', encoding='latin-1') as f:
    lector = csv.DictReader(f)
    for fila in lector:
        texto = ', '.join([f"{k}: {v}" for k, v in fila.items() if v])
        documentos.append(texto)
        ids.append(f"csv_{contador}")
        metadatos.append({"tipo": "csv"})
        contador += 1
        contador_csv += 1

print(f"  {contador_csv} filas cargadas del CSV")

# Cargar PDF
print("Cargando contenido de asignaturas PDF...")
ruta_pdf = os.path.join(DATA_PATH, 'Contenido_asignaturas.pdf')
contador_pdf = 0
with pdfplumber.open(ruta_pdf) as pdf:
    for num_pagina, pagina in enumerate(pdf.pages):
        texto = pagina.extract_text()
        if texto and texto.strip():
            fragmentos = [texto[i:i+800] for i in range(0, len(texto), 800)]
            for fragmento in fragmentos:
                if fragmento.strip():
                    documentos.append(fragmento)
                    ids.append(f"pdf_{contador}")
                    metadatos.append({"tipo": "pdf", "pagina": str(num_pagina)})
                    contador += 1
                    contador_pdf += 1

print(f"  {contador_pdf} fragmentos cargados del PDF")

# Generar embeddings
print(f"\nGenerando embeddings para {len(documentos)} documentos...")

LOTE = 50
for i in range(0, len(documentos), LOTE):
    lote_docs = documentos[i:i+LOTE]
    lote_ids = ids[i:i+LOTE]
    lote_meta = metadatos[i:i+LOTE]
    embeddings = modelo.encode(lote_docs).tolist()

    coleccion.add(
        documents=lote_docs,
        embeddings=embeddings,
        ids=lote_ids,
        metadatas=lote_meta
    )
    print(f"  Procesados {min(i+LOTE, len(documentos))}/{len(documentos)}")

print(f"\nCarga completada exitosamente")
print(f"Total documentos en ChromaDB: {coleccion.count()}")