from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db
from app.auth import get_current_user, get_current_admin_user

router = APIRouter()

# Rutas públicas (para guests)
@router.get("/profesores/", response_model=list[schemas.Profesor])
def read_profesores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    profesores = crud.get_profesores(db, skip=skip, limit=limit)
    return profesores

@router.get("/profesores/{profesor_id}", response_model=schemas.Profesor)
def read_profesor(profesor_id: int, db: Session = Depends(get_db)):
    profesor = crud.get_profesor(db, profesor_id=profesor_id)
    if profesor is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor

@router.get("/horarios/", response_model=list[schemas.Horario])
def read_horarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    horarios = crud.get_horarios(db, skip=skip, limit=limit)
    return horarios

@router.get("/horarios/{horario_id}", response_model=schemas.Horario)
def read_horario(horario_id: int, db: Session = Depends(get_db)):
    horario = crud.get_horario(db, horario_id=horario_id)
    if horario is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

@router.get("/profesores/{profesor_id}/horarios", response_model=list[schemas.Horario])
def read_horarios_profesor(profesor_id: int, db: Session = Depends(get_db)):
    horarios = crud.get_horarios_by_profesor(db, profesor_id=profesor_id)
    return horarios

# Rutas protegidas (solo admin)
@router.post("/profesores/", response_model=schemas.Profesor)
def create_profesor(
    profesor: schemas.ProfesorCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(get_current_admin_user)
):
    return crud.create_profesor(db=db, profesor=profesor)

@router.post("/horarios/", response_model=schemas.Horario)
def create_horario(
    horario: schemas.HorarioCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(get_current_admin_user)
):
    return crud.create_horario(db=db, horario=horario)

@router.delete("/horarios/{horario_id}")
def delete_horario(
    horario_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(get_current_admin_user)
):
    if not crud.delete_horario(db=db, horario_id=horario_id):
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return {"message": "Horario eliminado correctamente"}

@router.put("/profesores/{profesor_id}", response_model=schemas.Profesor)
def update_profesor(
    profesor_id: int,
    profesor: schemas.ProfesorCreate,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(get_current_admin_user)
):
    db_profesor = crud.update_profesor(db, profesor_id, profesor)
    if not db_profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return db_profesor

@router.delete("/profesores/{profesor_id}")
def delete_profesor(
    profesor_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(get_current_admin_user)
):
    if not crud.delete_profesor(db, profesor_id):
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return {"message": "Profesor eliminado correctamente"}

@router.put("/horarios/{horario_id}", response_model=schemas.Horario)
def update_horario(
    horario_id: int,
    horario: schemas.HorarioCreate,
    db: Session = Depends(get_db),
    current_user: schemas.Usuario = Depends(get_current_admin_user)
):
    db_horario = crud.update_horario(db, horario_id, horario)
    if not db_horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return db_horario
