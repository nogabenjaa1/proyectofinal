import streamlit as st
import requests
import pandas as pd
from collections import defaultdict

API_URL = "http://localhost:8000"

st.title("🎓 Sistema de Gestión Académica")

if "token" not in st.session_state:
    st.session_state.token = None
if "guest_mode" not in st.session_state:
    st.session_state.guest_mode = False

if not st.session_state.token and not st.session_state.guest_mode:
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("🔐 Iniciar sesión como Admin"):
            email = st.text_input("Correo", key="login_email")
            password = st.text_input("Contraseña", type="password", key="login_pwd")
            if st.button("Iniciar"):
                res = requests.post(f"{API_URL}/token", data={"username": email, "password": password})
                if res.status_code == 200:
                    st.session_state.token = res.json()["access_token"]
                    st.session_state.guest_mode = False
                    st.success("✅ Sesión iniciada como administrador")
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
    with col2:
        st.markdown("### ¿Solo quieres consultar?")
        if st.button("Entrar como invitado"):
            st.session_state.token = None
            st.session_state.guest_mode = True
            st.rerun()


if st.session_state.token:
    st.info("🔐 Estás en modo **Administrador**")
elif st.session_state.guest_mode:
    st.warning("🔓 Estás en modo **Invitado** (solo lectura)")
else:
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}

tab1, tab2, tab3 = st.tabs(["👨‍🏫 Profesores", "📅 Horarios", "⚙️ Utilidades"])

with tab1:
    st.subheader("Lista de Profesores")
    profs = requests.get(f"{API_URL}/api/profesores/", headers=headers).json()
    for p in profs:
        st.write(f"[{p['id']}] {p['nombre']} - {p['departamento'] or 'Sin depto'}")

    if st.session_state.token:
        st.divider()
        st.markdown("### ✏️ Editar / Eliminar Profesor")

        prof_opciones = {f"{p['nombre']} (ID: {p['id']})": p['id'] for p in profs}
        if prof_opciones:
            selected_prof = st.selectbox("Selecciona profesor", list(prof_opciones.keys()), key="edit_prof")
            selected_prof_id = prof_opciones[selected_prof]

            nuevo_nombre = st.text_input("Nuevo nombre", key="edit_nombre")
            nuevo_depto = st.text_input("Nuevo departamento", key="edit_depto")

            if st.button("Actualizar Profesor"):
                payload = {}
                if nuevo_nombre:
                    payload["nombre"] = nuevo_nombre
                if nuevo_depto:
                    payload["departamento"] = nuevo_depto

                if payload:
                    r = requests.put(f"{API_URL}/api/profesores/{selected_prof_id}", json=payload, headers=headers)
                    if r.status_code == 200:
                        st.success("✅ Profesor actualizado correctamente")
                        st.rerun()
                    else:
                        st.error("❌ Error al actualizar profesor")
                else:
                    st.warning("⚠️ No ingresaste ningún cambio")

            if st.button("Eliminar Profesor"):
                r = requests.delete(f"{API_URL}/api/profesores/{selected_prof_id}", headers=headers)
                if r.status_code == 200:
                    st.success("✅ Profesor eliminado")
                    st.rerun()
                else:
                    st.error("❌ Profesor no encontrado")
        else:
            st.info("No hay profesores registrados todavía")

        st.divider()
        st.markdown("### ➕ Crear nuevo Profesor")
        nuevo_nombre2 = st.text_input("Nombre", key="np")
        nuevo_depto2 = st.text_input("Departamento", key="dp")
        if st.button("Crear Profesor"):
            payload = {"nombre": nuevo_nombre2, "departamento": nuevo_depto2}
            r = requests.post(f"{API_URL}/api/profesores/", json=payload, headers=headers)
            if r.status_code == 200:
                st.success("✅ Profesor creado")
                st.rerun()
            else:
                st.error("❌ Error al crear profesor")

with tab2:
    from datetime import datetime, timedelta

    st.subheader("🗓️ Horario semanal por profesor")

    hs = requests.get(f"{API_URL}/api/horarios/", headers=headers).json()
    profs = requests.get(f"{API_URL}/api/profesores/", headers=headers).json()

    DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    profesores_map = {p["id"]: p for p in profs}
    horarios_por_prof = defaultdict(list)

    for h in hs:
        horarios_por_prof[h["profesor"]["id"]].append(h)

    profesores_ids = [pid for pid in horarios_por_prof if horarios_por_prof[pid]]

    if "prof_index" not in st.session_state:
        st.session_state.prof_index = 0

    if profesores_ids:
        if st.session_state.prof_index >= len(profesores_ids):
            st.session_state.prof_index = 0

        if len(profesores_ids) > 1:
            col1, _, col3 = st.columns([1, 3, 1])
            with col1:
                if st.button("⬅️ Anterior") and st.session_state.prof_index > 0:
                    st.session_state.prof_index -= 1
            with col3:
                if st.button("Siguiente ➡️") and st.session_state.prof_index < len(profesores_ids) - 1:
                    st.session_state.prof_index += 1

        pid = profesores_ids[st.session_state.prof_index]
        profe = profesores_map[pid]
        nombre = profe["nombre"]
        bloques = horarios_por_prof[pid]
        entrada = profe.get("hora_entrada") or "07:00:00"
        salida = profe.get("hora_salida") or "17:00:00"

        st.markdown(f"### 👨‍🏫 Horario de **{nombre}**")

        hora_i = datetime.strptime(entrada, "%H:%M:%S")
        hora_f = datetime.strptime(salida, "%H:%M:%S")
        horas = []
        actual = hora_i
        while actual < hora_f:
            horas.append(actual.time())
            actual += timedelta(hours=1)

        index = [f"{h.strftime('%H:%M')} - {(datetime.combine(datetime.today(), h) + timedelta(hours=1)).strftime('%H:%M')}" for h in horas]
        data = {dia: [""] * len(horas) for dia in DAYS}

        for h in bloques:
            dia = h["dia_semana"]
            hi = datetime.strptime(h["hora_inicio"], "%H:%M:%S").time()
            hf = datetime.strptime(h["hora_fin"], "%H:%M:%S").time()
            label = f"{h['asignatura']} ({h['aula']})"
            for idx, slot in enumerate(horas):
                slot_inicio = slot
                slot_fin = (datetime.combine(datetime.today(), slot) + timedelta(hours=1)).time()
                if hi < slot_fin and hf > slot_inicio and dia in DAYS:
                    data[dia][idx] = label

        df = pd.DataFrame(data, index=index)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay horarios cargados todavía.")

    st.divider()
    st.markdown("### ✏️ Editar / Eliminar Horarios")

    if st.session_state.token and hs:
        agrupados = defaultdict(list)
        for h in hs:
            clave = f"{h['asignatura']} - {h['profesor']['nombre']} (Aula {h['aula']})"
            agrupados[clave].append(h)

        seleccion = st.selectbox("Selecciona grupo de horarios", list(agrupados.keys()), key="edit_grupo")
        grupo = agrupados[seleccion]
        base = grupo[0]

        prof_opciones = {f"{p['nombre']} (ID: {p['id']})": p['id'] for p in profs}
        profe_sel = st.selectbox("Profesor", list(prof_opciones.keys()), key="edit_multi_prof")
        prof_id = prof_opciones[profe_sel]

        nueva_asig = st.text_input("Asignatura", value=base["asignatura"], key="edit_multi_asig")
        nueva_aula = st.text_input("Aula", value=base["aula"], key="edit_multi_aula")

        horarios_dias = {}
        for h in grupo:
            dia = h["dia_semana"]
            col1, col2 = st.columns(2)
            with col1:
                hi = st.time_input(f"Inicio - {dia}", value=datetime.strptime(h["hora_inicio"], "%H:%M:%S").time(), key=f"hi_{dia}")
            with col2:
                hf = st.time_input(f"Fin - {dia}", value=datetime.strptime(h["hora_fin"], "%H:%M:%S").time(), key=f"hf_{dia}")
            horarios_dias[dia] = (hi, hf)

        cols = st.columns([1, 1])
        with cols[0]:
            if st.button("💾 Actualizar días seleccionados"):
                success = 0
                for h in grupo:
                    dia = h["dia_semana"]
                    hi, hf = horarios_dias[dia]
                    payload = {
                        "profesor_id": prof_id,
                        "dia_semana": dia,
                        "hora_inicio": str(hi),
                        "hora_fin": str(hf),
                        "asignatura": nueva_asig,
                        "aula": nueva_aula
                    }
                    r = requests.put(f"{API_URL}/api/horarios/{h['id']}", json=payload, headers=headers)
                    if r.status_code == 200:
                        success += 1
                if success:
                    st.success(f"✅ Se actualizaron {success} horarios.")
                    st.rerun()
                else:
                    st.warning("⚠️ No se realizaron cambios")
        with cols[1]:
            if st.button("🗑️ Eliminar todos los horarios de este grupo"):
                eliminados = 0
                for h in grupo:
                    r = requests.delete(f"{API_URL}/api/horarios/{h['id']}", headers=headers)
                    if r.status_code == 200:
                        eliminados += 1
                if eliminados:
                    st.success(f"🗑️ Se eliminaron {eliminados} horario(s)")
                    st.rerun()
                else:
                    st.error("❌ No se pudieron eliminar los horarios")

    st.divider()
    st.markdown("### ➕ Crear nuevo Horario")

    if profs:
        prof_opciones = {f"{p['nombre']} (ID: {p['id']})": p['id'] for p in profs}
        nuevo_prof = st.selectbox("Profesor", list(prof_opciones.keys()), key="create_hr_prof")
        nuevo_prof_id = prof_opciones[nuevo_prof]

        dias_seleccionados = st.multiselect("Días en los que se imparte la asignatura", DAYS, key="dias_multi")
        horarios_dias = {}

        for dia in dias_seleccionados:
            st.markdown(f"**⏰ Horario para {dia}:**")
            col1, col2 = st.columns(2)
            with col1:
                inicio = st.time_input(f"Inicio - {dia}", key=f"start_{dia}")
            with col2:
                fin = st.time_input(f"Fin - {dia}", key=f"end_{dia}")
            horarios_dias[dia] = (inicio, fin)

        mat = st.text_input("Asignatura", key="mat")
        aula = st.text_input("Aula", key="aul")

        if st.button("Crear Horarios"):
            errores = 0
            for dia, (hi, hf) in horarios_dias.items():
                payload = {
                    "profesor_id": nuevo_prof_id,
                    "dia_semana": dia,
                    "hora_inicio": str(hi),
                    "hora_fin": str(hf),
                    "asignatura": mat,
                    "aula": aula
                }
                r = requests.post(f"{API_URL}/api/horarios/", json=payload, headers=headers)
                if r.status_code != 200:
                    errores += 1
            if errores == 0:
                st.success("✅ Todos los horarios fueron creados correctamente")
                st.rerun()
            else:
                st.warning(f"⚠️ Se creó la mayoría, pero hubo {errores} error(es)")
    else:
        st.warning("⚠️ Debes tener al menos un profesor para crear horarios.")

with tab3:
    st.markdown("### 🧹 Cerrar sesión / Cambiar modo")
    if st.button("Cerrar sesión"):
        st.session_state.token = None
        st.session_state.guest_mode = False
        st.success("👋 Sesión cerrada correctamente")
        st.rerun()


if st.button("🔄 Refrescar datos"):
    st.rerun()
