from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_db

router = APIRouter()

class MateriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = ""

class MateriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

@router.get("/")
def listar_materias(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM academico.materia")
    return cursor.fetchall()

@router.get("/{materia_id}")
def obtener_materia(materia_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM academico.materia WHERE materia_id = %s", (materia_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return row

@router.post("/", status_code=201)
def crear_materia(data: MateriaCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO academico.materia (nombre, descripcion) VALUES (%s, %s)",
        (data.nombre, data.descripcion)
    )
    db.commit()
    return {"message": "Materia creada", "id": cursor.lastrowid}

@router.put("/{materia_id}")
def actualizar_materia(materia_id: int, data: MateriaUpdate, db=Depends(get_db)):
    campos = {k: v for k, v in data.dict().items() if v is not None}
    if not campos:
        raise HTTPException(status_code=400, detail="Sin datos para actualizar")
    set_clause = ", ".join([f"{k} = %s" for k in campos])
    cursor = db.cursor()
    cursor.execute(
        f"UPDATE academico.materia SET {set_clause} WHERE materia_id = %s",
        (*campos.values(), materia_id)
    )
    db.commit()
    return {"message": "Materia actualizada"}

@router.delete("/{materia_id}")
def eliminar_materia(materia_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM academico.materia WHERE materia_id = %s", (materia_id,))
    db.commit()
    return {"message": "Materia eliminada"}
