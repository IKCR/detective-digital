from flask import Flask, request
import unicodedata

app = Flask(__name__)

def normalizar(texto):
    texto = texto.strip().lower()
    texto = texto.rstrip(".,!?")
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto

INTRODUCCION_GENERAL = (
    "Bienvenido a DETECTIVE DIGITAL.\n\n"
    "Eres un analista forense de ciberseguridad. Tu trabajo es investigar incidentes "
    "que ya ocurrieron, encontrar al responsable, seguir las pistas que deja (algunas "
    "reales, otras falsas para despistarte) y corregir la falla de seguridad que "
    "permitio el ataque. Cada caso tiene 3 etapas: investigar, leer pistas del atacante "
    "y corregir la vulnerabilidad.\n\n"
    "Comandos disponibles:\n"
    "EXAMINAR <nombre> - revisa un registro o reporte\n"
    "INTERROGAR <algo> - consulta el estado de un sistema\n"
    "LEER_CARTA - lee el mensaje que dejo el atacante (disponible en la etapa 2)\n"
    "ACUSAR <respuesta> - senala al responsable o al lugar (etapas 1 y 2)\n"
    "PARCHAR <vulnerabilidad> - corrige la falla de seguridad (etapa 3)\n"
    "CERRAR_CASO - cierra el caso actual y pasa al siguiente\n"
    "AYUDA - vuelve a mostrar esta explicacion\n"
)

# ---------- LISTA DE CASOS ----------
casos = [
    {
        "titulo": "Caso 1: El Servidor Comprometido",
        "descripcion": (
            "Un servidor de la empresa fue comprometido anoche. El equipo de sistemas "
            "detecto actividad extrana y te llamaron a ti para investigar que paso, "
            "quien lo hizo y como evitar que vuelva a pasar. Empieza revisando los "
            "registros del servidor con EXAMINAR (prueba con log1, log2, log3 o log4)."
        ),
        "logs": {
            "log1": "01:02:13 - Usuario 'admin' inicio sesion desde 192.168.1.10 (uso normal).",
            "log2": "01:05:47 - Copia de seguridad automatica completada sin errores.",
            "log3": "01:07:52 - Intento de acceso fallido desde IP 45.33.22.156, 5 veces en 10 segundos.",
            "log4": "01:10:03 - Actualizacion de software completada en servidor1.",
        },
        "respuesta_investigacion": "45.33.22.156",
        "carta": (
            "Querido detective:\n\n"
            "Disfrute mucho ver como revisabas mis huellas en el SOTANO del edificio, "
            "aunque la verdad es que ahi solo fui una vez a dejarte algo de diversion. "
            "Si de verdad quieres encontrarme, deberias mirar con mas calma el reporte "
            "de mantenimiento de la AZOTEA, ahi paso mas tiempo del que crees.\n\n"
            "Diviertete buscando.\n"
        ),
        "respuesta_lugar": "azotea",
        "trampa_lugar": "sotano",
        "nombre_reporte": "reporte_azotea",
        "reporte": "Inspeccion de la azotea: se encontro un router de mantenimiento con PUERTO_22 abierto hacia internet, aunque revisando bien el historial ese puerto ya estaba cerrado desde hace meses. Lo que si llama la atencion es que el router seguia usando la CONTRASENA_DEBIL de fabrica, nunca fue cambiada.",
        "respuesta_vulnerabilidad": "contrasena_debil",
        "trampa_vulnerabilidad": "puerto_22",
    },
    {
        "titulo": "Caso 2: La Fuga de Datos",
        "descripcion": (
            "La empresa detecto que informacion confidencial de clientes aparecio "
            "filtrada en internet. Alguien de adentro pudo haber sido el responsable. "
            "Revisa los registros de acceso para descubrir quien fue (EXAMINAR log1, "
            "log2, log3 o log4)."
        ),
        "logs": {
            "log1": "08:15:02 - Usuario 'carla_mendez' inicio sesion desde su equipo habitual.",
            "log2": "08:40:19 - Impresora del piso 3 reporto atasco de papel (evento comun).",
            "log3": "23:47:31 - Usuario 'carla_mendez' descargo 4.2 GB de la base de datos de clientes a las 11:47 PM, fuera de su horario habitual.",
            "log4": "09:02:44 - Actualizacion mensual de antivirus completada.",
        },
        "respuesta_investigacion": "carla_mendez",
        "carta": (
            "Hola de nuevo, detective:\n\n"
            "Que buen trabajo encontrando a mi 'colaboradora'. Por cierto, si buscas "
            "la informacion que se llevo, no pierdas el tiempo revisando su CORREO "
            "personal, ahi no vas a encontrar nada util. Lo que deberias revisar es "
            "su USB, la tiene guardada en el cajon de su escritorio.\n\n"
            "Buena suerte.\n"
        ),
        "respuesta_lugar": "usb",
        "trampa_lugar": "correo",
        "nombre_reporte": "reporte_escritorio",
        "reporte": "Inspeccion del escritorio: se reviso el equipo y se confirmo que la CUENTA_COMPARTIDA del departamento tenia acceso a la base de datos sin necesitar permisos individuales, lo cual no deberia ser posible. Tambien se noto que el ANTIVIRUS estaba desactualizado, aunque la version que tenia si detectaba este tipo de transferencias.",
        "respuesta_vulnerabilidad": "cuenta_compartida",
        "trampa_vulnerabilidad": "antivirus",
    },
]

ESTILO = """
<style>
body {
    background-color: #0d1117;
    color: #39ff14;
    font-family: 'Courier New', monospace;
    margin: 0;
    padding: 0;
}
.contenedor {
    max-width: 720px;
    margin: 40px auto;
    padding: 30px 35px;
    background-color: #111820;
    border: 1px solid #1f2937;
    border-radius: 10px;
    box-shadow: 0 0 25px rgba(57, 255, 20, 0.12);
}
h1 {
    margin: 0 0 5px 0;
    font-size: 26px;
    letter-spacing: 1px;
    border-bottom: 2px solid #1f2937;
    padding-bottom: 12px;
}
.subtitulo {
    color: #7ee787;
    font-size: 13px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 20px;
}
.info-caso {
    background-color: #0d1117;
    border-left: 4px solid #39ff14;
    padding: 10px 15px;
    font-size: 14px;
    color: #9ae6b4;
    margin-bottom: 20px;
}
form {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}
input[type=text] {
    flex: 1;
    background-color: #0d1117;
    border: 1px solid #39ff14;
    color: #39ff14;
    padding: 10px 12px;
    font-family: inherit;
    font-size: 14px;
    border-radius: 4px;
}
input[type=text]:focus {
    outline: none;
    box-shadow: 0 0 8px rgba(57, 255, 20, 0.5);
}
button {
    background-color: #39ff14;
    color: #0d1117;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
    font-family: inherit;
    border-radius: 4px;
    cursor: pointer;
}
button:hover {
    background-color: #2ecc71;
}
.caja-resultado {
    background-color: #0d1117;
    border: 1px solid #1f2937;
    border-left: 4px solid #39ff14;
    padding: 18px;
    white-space: pre-line;
    font-size: 14px;
    line-height: 1.5;
    color: #c9f7c9;
    border-radius: 4px;
}
.puntaje {
    margin-top: 18px;
    font-size: 15px;
    font-weight: bold;
    color: #39ff14;
}
</style>
"""

# ---------- Estado del juego ----------
puntaje = 0
caso_index = 0
fase = 1
parchado = False
juego_terminado = False

@app.route("/", methods=["GET", "POST"])
def inicio():
    global puntaje, caso_index, fase, parchado, juego_terminado
    resultado = ""
    caso = casos[caso_index] if caso_index < len(casos) else None

    if request.method == "GET":
        resultado = INTRODUCCION_GENERAL + "\n" + caso["descripcion"]

    elif request.method == "POST" and not juego_terminado:
        instruccion = request.form.get("instruccion", "")
        partes = instruccion.strip().split(" ", 1)
        comando = normalizar(partes[0]).upper() if len(partes) > 0 else ""
        argumento = normalizar(partes[1]) if len(partes) > 1 else ""

        if comando == "AYUDA":
            resultado = INTRODUCCION_GENERAL

        elif comando == "EXAMINAR":
            if argumento in caso["logs"]:
                resultado = caso["logs"][argumento]
            elif argumento == caso["nombre_reporte"]:
                if fase >= 3:
                    resultado = caso["reporte"]
                else:
                    resultado = "Todavia no puedes examinar ese reporte. Resuelve primero el caso anterior."
            else:
                resultado = "No existe ningun registro llamado '" + argumento + "'."

        elif comando == "INTERROGAR":
            resultado = "Interrogando al sistema: " + argumento + "..."

        elif comando == "LEER_CARTA":
            if fase >= 2:
                resultado = caso["carta"]
            else:
                resultado = "Todavia no tienes acceso a ninguna carta. Resuelve primero la investigacion con ACUSAR."

        elif comando == "ACUSAR":
            if fase == 1:
                if argumento == normalizar(caso["respuesta_investigacion"]):
                    puntaje = puntaje + 10
                    fase = 2
                    resultado = "Correcto! Caso resuelto en la etapa de investigacion. Puntaje: " + str(puntaje) + ". Prueba LEER_CARTA."
                else:
                    puntaje = puntaje - 5
                    resultado = "Acusacion incorrecta. Revisa mejor los registros. Puntaje: " + str(puntaje)

            elif fase == 2:
                if argumento == caso["respuesta_lugar"]:
                    puntaje = puntaje + 10
                    fase = 3
                    resultado = "Correcto! Prueba ahora EXAMINAR " + caso["nombre_reporte"] + ". Puntaje: " + str(puntaje)
                elif argumento == caso["trampa_lugar"]:
                    puntaje = puntaje - 10
                    resultado = "Caiste en una pista falsa. El atacante te engano. Puntaje: " + str(puntaje)
                else:
                    puntaje = puntaje - 5
                    resultado = "Acusacion incorrecta. Revisa mejor la carta. Puntaje: " + str(puntaje)

            else:
                resultado = "Ya no hay mas acusaciones pendientes. Prueba con PARCHAR."

        elif comando == "PARCHAR":
            if fase != 3:
                resultado = "Todavia no puedes parchar nada en esta etapa."
            else:
                if argumento == caso["respuesta_vulnerabilidad"]:
                    puntaje = puntaje + 15
                    parchado = True
                    resultado = "Correcto! Vulnerabilidad corregida. Puntaje: " + str(puntaje) + ". Ahora escribe CERRAR_CASO."
                elif argumento == caso["trampa_vulnerabilidad"]:
                    puntaje = puntaje - 10
                    resultado = "Esa no era la vulnerabilidad real, perdiste tiempo. Puntaje: " + str(puntaje)
                else:
                    puntaje = puntaje - 5
                    resultado = "Esa no es una vulnerabilidad valida. Revisa bien el reporte. Puntaje: " + str(puntaje)

        elif comando == "CERRAR_CASO":
            if parchado:
                if caso_index + 1 < len(casos):
                    caso_index = caso_index + 1
                    fase = 1
                    parchado = False
                    nuevo_caso = casos[caso_index]
                    resultado = "Caso cerrado. Puntaje: " + str(puntaje) + ".\n\n" + nuevo_caso["titulo"] + "\n" + nuevo_caso["descripcion"]
                else:
                    juego_terminado = True
                    resultado = "Ultimo caso cerrado. Juego completado. Puntaje final: " + str(puntaje)
            else:
                resultado = "Todavia no puedes cerrar el caso. Aun faltan pasos por resolver."

        else:
            resultado = "Comando no reconocido. Escribe AYUDA para ver la lista de comandos."

    elif juego_terminado:
        resultado = "El juego ya esta terminado. Puntaje final: " + str(puntaje)

    titulo_caso = casos[caso_index]["titulo"] if caso_index < len(casos) else "Juego terminado"

    pagina = "<html><head>" + ESTILO + "</head><body>"
    pagina += "<div class='contenedor'>"
    pagina += "<h1>DETECTIVE DIGITAL</h1>"
    pagina += "<div class='subtitulo'>Unidad de Investigacion Forense Digital</div>"
    pagina += "<div class='info-caso'>" + titulo_caso + " &mdash; Fase " + str(fase) + "</div>"
    pagina += "<form method='POST' autocomplete='off'>"
    pagina += "<input type='text' name='instruccion' placeholder='Escribe una instruccion...' autocomplete='off' spellcheck='false'>"
    pagina += "<button type='submit'>Enviar</button>"
    pagina += "</form>"
    pagina += "<div class='caja-resultado'>" + resultado + "</div>"
    pagina += "<div class='puntaje'>Puntaje actual: " + str(puntaje) + "</div>"
    pagina += "</div>"
    pagina += "</body></html>"

    return pagina

if __name__ == "__main__":
    app.run(debug=True)