from fastapi import APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import User
from schemas.user_schema import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

# Crear usuario
@router.post("/")
def crear_usuario(user: UserCreate):
    db: Session = SessionLocal()

    nuevo = User(nombre=user.nombre, email=user.email)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo

# Obtener usuarios
@router.get("/")
def obtener_usuarios():
    db: Session = SessionLocal()
    return db.query(User).all()