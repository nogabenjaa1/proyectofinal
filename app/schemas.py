from pydantic import BaseModel, EmailStr
from datetime import time
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UsuarioBase(BaseModel):
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    es_admin: bool

    class Config:
        from_attributes = True

class ProfesorBase(BaseModel):
    nombre: str
    departamento: Optional[str] = None
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None

class ProfesorCreate(ProfesorBase):
    pass

class Profesor(ProfesorBase):
    id: int

    class Config:
        from_attributes = True

class ProfesorUpdate(BaseModel):
    nombre: Optional[str] = None
    departamento: Optional[str] = None
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None

class HorarioBase(BaseModel):
    profesor_id: int
    dia_semana: str
    hora_inicio: time
    hora_fin: time
    asignatura: str
    aula: str

class HorarioCreate(HorarioBase):
    pass

class Horario(HorarioBase):
    id: int
    profesor: Profesor

    class Config:
        from_attributes = True

class HorarioUpdate(BaseModel):
    profesor_id: Optional[int] = None
    dia_semana: Optional[str] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    asignatura: Optional[str] = None
    aula: Optional[str] = None
