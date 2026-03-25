from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db

router = APIRouter()

class CalificacionCreate(BaseModel):
    inscripcion_id: int
    parcial1: float
    parcial2: float
    parcial3: float

class CalificacionUpdate(BaseModel):
    parcial1: Optional[float] = None
    parcial2: Optional[float] = None
    parcial3: Optional[float] = None

def calcular_promedio(p1, p2, p3):
    vals = [v for v in [p1, p2, p3] if v is not None]
    return round(sum(vals) / len(vals), 2) if vals else 0

@router.get("/")
def listar_calificaciones(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, e.nombre as estudiante, m.nombre as materia
        FROM evaluacion.calificacion_materia c
        JOIN estudiantes.inscripcion_materia i ON c.inscripcion_id = i.inscripcion_id
        JOIN estudiantes.estudiante e ON i.estudiante_id = e.estudiante_id
        JOIN academico.materia m ON i.materia_id = m.materia_id
    """)
    return cursor.fetchall()

@router.get("/estudiante/{estudiante_id}")
def calificaciones_por_estudiante(estudiante_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, m.nombre as materia
        FROM evaluacion.calificacion_materia c
        JOIN estudiantes.inscripcion_materia i ON c.inscripcion_id = i.inscripcion_id
        JOIN academico.materia m ON i.materia_id = m.materia_id
        WHERE i.estudiante_id = %s
    """, (estudiante_id,))
    return cursor.fetchall()

@router.post("/", status_code=201)
def crear_calificacion(data: CalificacionCreate, db=Depends(get_db)):
    promedio = calcular_promedio(data.parcial1, data.parcial2, data.parcial3)
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO evaluacion.calificacion_materia (inscripcion_id, parcial1, parcial2, parcial3, promedio)
        VALUES (%s, %s, %s, %s, %s)
    """, (data.inscripcion_id, data.parcial1, data.parcial2, data.parcial3, promedio))
    db.commit()
    return {"message": "Calificación registrada", "id": cursor.lastrowid, "promedio": promedio}

@router.put("/{calificacion_id}")
def actualizar_calificacion(calificacion_id: int, data: CalificacionUpdate, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM evaluacion.calificacion_materia WHERE calificacion_id = %s", (calificacion_id,))
    actual = cursor.fetchone()
    if not actual:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    p1 = data.parcial1 if data.parcial1 is not None else actual["parcial1"]
    p2 = data.parcial2 if data.parcial2 is not None else actual["parcial2"]
    p3 = data.parcial3 if data.parcial3 is not None else actual["parcial3"]
    promedio = calcular_promedio(p1, p2, p3)
    cursor2 = db.cursor()
    cursor2.execute("""
        UPDATE evaluacion.calificacion_materia
        SET parcial1=%s, parcial2=%s, parcial3=%s, promedio=%s
        WHERE calificacion_id=%s
    """, (p1, p2, p3, promedio, calificacion_id))
    db.commit()
    return {"message": "Calificación actualizada", "promedio": promedio}

@router.delete("/{calificacion_id}")
def eliminar_calificacion(calificacion_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM evaluacion.calificacion_materia WHERE calificacion_id = %s", (calificacion_id,))
    db.commit()
    return {"message": "Calificación eliminada"}
