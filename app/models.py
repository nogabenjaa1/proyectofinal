from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    es_admin = Column(Boolean, default=False)

class Profesor(Base):
    __tablename__ = "profesores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    departamento = Column(String)
    hora_entrada = Column(Time)
    hora_salida = Column(Time)

class Horario(Base):
    __tablename__ = "horarios"
    
    id = Column(Integer, primary_key=True, index=True)
    profesor_id = Column(Integer, ForeignKey("profesores.id"))
    dia_semana = Column(String)  
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    asignatura = Column(String)
    aula = Column(String)

    profesor = relationship("Profesor")
