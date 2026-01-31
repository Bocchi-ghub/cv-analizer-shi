from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
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
async def analizar_curriculum(file: UploadFile = File(...)):
    """
    Esta ruta recibe el PDF.
    Por ahora, solo te dirá el nombre del archivo y el tipo.
    """
    # 1. Validamos que sea un PDF
    if file.content_type != "application/pdf":
        return {"error": "El archivo debe ser un PDF"}
    
    # 2. Aquí iría la lógica de extracción de texto (lo haremos en el siguiente paso)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "mensaje": "Archivo recibido con éxito. Listo para procesar."
    }