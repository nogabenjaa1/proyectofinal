# 🎓 Sistema de Gestión Académica

Este sistema permite crear, consultar, editar y eliminar horarios académicos asignados a profesores a lo largo de la semana. Desarrollado con **FastAPI** y **Streamlit**, está diseñado para ser simple, visual y funcional.

---

## 🧭 Navegación General

La aplicación tiene 3 pestañas principales:

- 👨‍🏫 **Profesores**  
  Gestiona la lista de profesores registrados.

- 📅 **Horarios**  
  Crea horarios por asignatura/día, edita bloques múltiples, y muestra tablas semanales por profesor.

- ⚙️ **Utilidades**  
  Permite cerrar sesión o cambiar de modo entre administrador e invitado.

---

## 🔐 Autenticación

- Inicia sesión como **Administrador** ingresando tu correo y contraseña. Email: nogabenstudent@owner.io Password: notbenjaa1
- Puedes entrar como **Invitado** (solo lectura).
- Una vez logueado, el bloque de login desaparece para liberar espacio.

---

## 👨‍🏫 Profesores

### Crear nuevo profesor

1. Ve a la pestaña `👨‍🏫 Profesores`.
2. Llena los campos `Nombre` y `Departamento`.
3. Haz clic en `Crear Profesor`.

### Editar o eliminar un profesor existente

1. Selecciona un profesor de la lista.
2. Ingresa nuevos datos si deseas editar.
3. Haz clic en `Actualizar Profesor` o `Eliminar Profesor`.

⚠️ Solo administradores pueden modificar esta sección.

---

## 📅 Horarios

### Crear horario

1. Selecciona un profesor.
2. Selecciona los días (puedes escoger varios).
3. Para cada día, indica hora de inicio y fin.
4. Agrega la `Asignatura` y el `Aula`.
5. Haz clic en `Crear Horarios`.

> Cada día genera un bloque horario independiente.

---

### Ver horarios por profesor (modo semanal)

- Se muestra una **tabla horizontal** tipo calendario escolar.
- Aparecen solo profesores con horarios asignados.
- Usa los botones `⬅️` y `➡️` para moverte entre ellos si hay varios.

---

### Editar múltiples horarios

1. Selecciona un grupo de horarios por `Asignatura`, `Profesor` y `Aula`.
2. Cambia horas para cada día afectado.
3. Opcional: cambia el nombre de la asignatura, aula o profesor.
4. Haz clic en `Actualizar días seleccionados`.

También puedes eliminar todos los días del grupo desde el mismo bloque.

---

## ⚙️ Utilidades

Desde la pestaña `⚙️ Utilidades` puedes:

- Cerrar sesión como admin
- Cambiar de modo administrador a invitado (y viceversa)
- Navegar sin ver el bloque de login una vez dentro

---

## 🛠️ Requisitos técnicos

- Python 3.10+
- FastAPI + Uvicorn
- Streamlit
- requests, pandas

---

## 💡 Notas extra

- Al actualizar o eliminar un horario o profesor, los cambios se reflejan al instante (`st.rerun()` incluido).
- Puedes registrar profesores con su hora de entrada y salida para generar automáticamente su tabla semanal.

---
