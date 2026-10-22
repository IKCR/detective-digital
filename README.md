# Detective Digital

Máquina virtual temática de ciberseguridad defensiva (blue team) desarrollada para la materia **Seguridad en la Nube**, Ingeniería de Sistemas y Computación, Universidad de Cundinamarca.

**Autora:** Ingrid Katherin Caicedo Rodríguez

## De qué trata

El jugador es un analista forense digital. Cada caso es un incidente de seguridad que ya ocurrió: hay que investigar los registros, encontrar al responsable, interpretar las pistas del atacante (algunas reales y otras falsas) y corregir la vulnerabilidad que permitió el ataque.

## Cómo se juega

Cada caso tiene 3 fases:

1. **Investigación:** se examinan registros (logs) hasta encontrar la pista real entre el ruido, y se acusa al responsable.
2. **Pistas del atacante:** se lee la carta del atacante, que mezcla una pista falsa con la real, y se acusa el lugar correcto.
3. **Remediación:** se examina el reporte técnico, se parcha la vulnerabilidad real (no el señuelo) y se cierra el caso.

## Comandos

- `EXAMINAR <nombre>`: revisa un registro o reporte.
- `INTERROGAR <sistema>`: consulta el estado de un sistema.
- `LEER_CARTA`: muestra el mensaje del atacante (desde la fase 2).
- `ACUSAR <respuesta>`: señala al responsable (fase 1) o al lugar (fase 2).
- `PARCHAR <vulnerabilidad>`: corrige la falla de seguridad (fase 3).
- `CERRAR_CASO`: cierra el caso actual y pasa al siguiente.
- `AYUDA`: vuelve a mostrar la introducción y los comandos.

## Puntaje

- Acierto en investigación: +10
- Acierto en el lugar: +10
- Vulnerabilidad real corregida: +15
- Acusación incorrecta: -5
- Caer en una pista falsa: -10

## Tecnologías

- Python 3
- Flask
- HTML y CSS (interfaz tipo terminal)

## Cómo ejecutarlo

1. Instalar Flask: `pip install flask`
2. Ejecutar: `python app.py`
3. Abrir en el navegador: http://127.0.0.1:5000

## Estado del proyecto

- 2 casos jugables de principio a fin.
- Pendiente: más casos, información real en `INTERROGAR` y guardado del puntaje.
