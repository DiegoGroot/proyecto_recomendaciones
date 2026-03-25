from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from database import get_db

router = APIRouter()

class EstudianteCreate(BaseModel):
    nombre: str
    correo: str
    contrasena: str
    carrera_id: int

class EstudianteUpdate(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    carrera_id: Optional[int] = None

# GET todos
@router.get("/")
def listar_estudiantes(db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.estudiante_id, e.nombre, e.correo, e.carrera_id, c.nombre as carrera, e.creado_en
        FROM estudiantes.estudiante e
        LEFT JOIN academico.carrera c ON e.carrera_id = c.carrera_id
    """)
    return cursor.fetchall()

# GET uno
@router.get("/{estudiante_id}")
def obtener_estudiante(estudiante_id: int, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.estudiante_id, e.nombre, e.correo, e.carrera_id, c.nombre as carrera, e.creado_en
        FROM estudiantes.estudiante e
        LEFT JOIN academico.carrera c ON e.carrera_id = c.carrera_id
        WHERE e.estudiante_id = %s
    """, (estudiante_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return row

# POST crear
@router.post("/", status_code=201)
def crear_estudiante(data: EstudianteCreate, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO estudiantes.estudiante (nombre, correo, contrasena, carrera_id)
        VALUES (%s, %s, %s, %s)
    """, (data.nombre, data.correo, data.contrasena, data.carrera_id))
    db.commit()
    return {"message": "Estudiante creado", "id": cursor.lastrowid}

# PUT actualizar
@router.put("/{estudiante_id}")
def actualizar_estudiante(estudiante_id: int, data: EstudianteUpdate, db=Depends(get_db)):
    campos = {k: v for k, v in data.dict().items() if v is not None}
    if not campos:
        raise HTTPException(status_code=400, detail="Sin datos para actualizar")
    set_clause = ", ".join([f"{k} = %s" for k in campos])
    cursor = db.cursor()
    cursor.execute(
        f"UPDATE estudiantes.estudiante SET {set_clause} WHERE estudiante_id = %s",
        (*campos.values(), estudiante_id)
    )
    db.commit()
    return {"message": "Estudiante actualizado"}

# DELETE
@router.delete("/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM estudiantes.estudiante WHERE estudiante_id = %s", (estudiante_id,))
    db.commit()
    return {"message": "Estudiante eliminado"}

# LOGIN simple
class LoginData(BaseModel):
    correo: str
    contrasena: str

@router.post("/login")
def login(data: LoginData, db=Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT estudiante_id, nombre, correo, carrera_id
        FROM estudiantes.estudiante
        WHERE correo = %s AND contrasena = %s
    """, (data.correo, data.contrasena))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"message": "Login exitoso", "estudiante": user}
