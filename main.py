import fitz  # PyMuPDF: Para analizar el pdf y extraer el texto
from fastapi import FastAPI, File, UploadFile 
from pydantic import BaseModel # Pydantic: Para control de errores en tipado y evitar problemas al recibir la información
from typing import List 

app = FastAPI(title="CV Analyzer Tool", version="1.0.0")

# --- MODELOS (Pydantic) ---
# Aquí definimos cómo queremos que la IA nos devuelva los datos después (lo usaremos pronto)
# Básicamente esta wea nos ayuda con el control de errores y mantener el tipado de los datos fijos para que se puedan analizar bien, si no, no entran 
class Candidato(BaseModel):
    nombre: str
    skills: List[str]
    años_experiencia: int

# --- ENDPOINTS (Rutas) ---

@app.get("/")
def home():
    """Ruta de prueba para ver si el servidor funciona"""
    return {"mensaje": "API de CV Analyzer funcionando correctamente"}

@app.post("/analizar-cv")
async def analizar_curriculum(file: UploadFile = File(...)):  #el async es pa que trabaje en paralelo 
    """
    Recibe el PDF, extrae el texto crudo y lo devuelve.
    """
    # 1. Validar PDF
    if file.content_type != "application/pdf":
        return {"error": "El archivo debe estar en formato PDF"}
    
    # 2. Leer el archivo en memoria (bytes)
    contenido_pdf = await file.read()
    
    # 3. Abrir el PDF con PyMuPDF
    # "stream" permite abrirlo desde la memoria RAM sin guardarlo en disco
    doc = fitz.open(stream=contenido_pdf, filetype="pdf")
    
    texto_completo = ""
    
    # 4. Recorrer cada página y extraer texto
    for pagina in doc:
        texto_completo += pagina.get_text() + "\n"
        
    # 5. Devolver el resultado
    return {
        "filename": file.filename,
        "total_paginas": len(doc),
        "texto_recuperado": texto_completo  # <--- En teoría está bien todo dentro de un string pq finalmente el analisis lo hará la IA. En caso de que quisieramos buscar x palabras clave, no hay necesidad de que sea una lista (?)
    }