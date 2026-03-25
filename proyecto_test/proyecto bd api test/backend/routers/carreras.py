from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db

router = APIRouter()

class CarreraCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = ""

class CarreraUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

@router.get("/")
def listar_carreras(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM academico.carrera")
    return cursor.fetchall()

@router.get("/{carrera_id}")
def obtener_carrera(carrera_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM academico.carrera WHERE carrera_id = %s", (carrera_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return row

@router.post("/", status_code=201)
def crear_carrera(data: CarreraCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO academico.carrera (nombre, descripcion) VALUES (%s, %s)",
        (data.nombre, data.descripcion)
    )
    db.commit()
    return {"message": "Carrera creada", "id": cursor.lastrowid}

@router.put("/{carrera_id}")
def actualizar_carrera(carrera_id: int, data: CarreraUpdate, db=Depends(get_db)):
    campos = {k: v for k, v in data.dict().items() if v is not None}
    if not campos:
        raise HTTPException(status_code=400, detail="Sin datos para actualizar")
    set_clause = ", ".join([f"{k} = %s" for k in campos])
    cursor = db.cursor()
    cursor.execute(
        f"UPDATE academico.carrera SET {set_clause} WHERE carrera_id = %s",
        (*campos.values(), carrera_id)
    )
    db.commit()
    return {"message": "Carrera actualizada"}

@router.delete("/{carrera_id}")
def eliminar_carrera(carrera_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM academico.carrera WHERE carrera_id = %s", (carrera_id,))
    db.commit()
    return {"message": "Carrera eliminada"}
