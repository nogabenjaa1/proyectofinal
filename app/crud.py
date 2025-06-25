from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = pwd_context.hash(usuario.password)
    db_usuario = models.Usuario(
        email=usuario.email, 
        hashed_password=hashed_password,
        es_admin=False
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def authenticate_usuario(db: Session, email: str, password: str):
    usuario = get_usuario_by_email(db, email)
    if not usuario:
        return False
    if not pwd_context.verify(password, usuario.hashed_password):
        return False
    return usuario

# Profesores
def get_profesor(db: Session, profesor_id: int):
    return db.query(models.Profesor).filter(models.Profesor.id == profesor_id).first()

def get_profesores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profesor).offset(skip).limit(limit).all()

def create_profesor(db: Session, profesor: schemas.ProfesorCreate):
    db_profesor = models.Profesor(**profesor.dict())
    db.add(db_profesor)
    db.commit()
    db.refresh(db_profesor)
    return db_profesor

def update_profesor(db: Session, profesor_id: int, data: schemas.ProfesorUpdate):
    db_profesor = db.query(models.Profesor).filter(models.Profesor.id == profesor_id).first()
    if not db_profesor:
        return None
    profesor_data = data.dict(exclude_unset=True)
    for attr, value in profesor_data.items():
        setattr(db_profesor, attr, value)
    db.commit()
    db.refresh(db_profesor)
    return db_profesor

def delete_profesor(db: Session, profesor_id: int):
    db_profesor = db.query(models.Profesor).filter(models.Profesor.id == profesor_id).first()
    if db_profesor:
        db.delete(db_profesor)
        db.commit()
        return True
    return False

# Horarios
def get_horario(db: Session, horario_id: int):
    return db.query(models.Horario).filter(models.Horario.id == horario_id).first()

def get_horarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Horario).offset(skip).limit(limit).all()

def get_horarios_by_profesor(db: Session, profesor_id: int):
    return db.query(models.Horario).filter(models.Horario.profesor_id == profesor_id).all()

def create_horario(db: Session, horario: schemas.HorarioCreate):
    db_horario = models.Horario(**horario.dict())
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario

def update_horario(db: Session, horario_id: int, data: schemas.HorarioUpdate):
    db_horario = db.query(models.Horario).filter(models.Horario.id == horario_id).first()
    if not db_horario:
        return None
    horario_data = data.dict(exclude_unset=True)
    for attr, value in horario_data.items():
        setattr(db_horario, attr, value)
    db.commit()
    db.refresh(db_horario)
    return db_horario

def delete_horario(db: Session, horario_id: int):
    db_horario = db.query(models.Horario).filter(models.Horario.id == horario_id).first()
    if db_horario:
        db.delete(db_horario)
        db.commit()
        return True
    return False
