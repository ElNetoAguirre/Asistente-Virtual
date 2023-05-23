"""
Asistente Virtual
"""

import datetime
import webbrowser
import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import wikipedia

# Opciones de Voz / Idioma
# Si no coloco la 'r', marca el error Pylint(W1401:anomalous-backslash-in-string)
ID1 = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"
ID2 = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

# Escuchar el micrófono y devolver el audio como texto
def transformar_audio_en_texto():
    """Escuchar el micrófono y devolver el audio como texto"""
    # Almacenar recognizer en variable
    r = sr.Recognizer()

    # Configurar el micrófono
    with sr.Microphone() as origen:
        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar que comenzó la grabación
        print("Ya Puedes comenzar a hablar")

        # Guardar lo capturado por el micrófono
        audio = r.listen(origen)

        try:
            # Buscar en Google
            pedido = r.recognize_google(audio, language="es-mx")
            # prueba de que se pudo ingresar
            print("Dijiste: " + pedido)
            # Devolver a pedido
            return pedido
        # En caso de que no comprenda el audio
        except sr.UnknownValueError:
            # Prueba de que no comprendio el audio
            print("Ups, no entendí...")
            # Devolver error
            return "Sigo esperando..."
        # En caso de no resolver el pedido
        except sr.RequestError:
            # Prueba de que no comprendio el audio
            print("Ups, no hay servicio...")
            # Devolver error
            return "Sigo esperando..."
        # En caso de error inesperado
        except AssertionError:
            # Prueba de que no comprendio el audio
            print("Ups, algo salió mal...")
            # Devolver error
            return "Sigo esperando..."

# Función para que el Asistente pueda ser escuchado
def hablar(mensaje):
    """Función para que el Asistente pueda ser escuchado"""
    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", ID1)
    # Pronunciar el mensaje
    engine.say(mensaje)
    engine.runAndWait()

# Informar el día de la semana
def pedir_dia():
    """Informar el día de la semana"""
    # Crear variable con los datos del día de hoy
    dia =  datetime.date.today()
    print(dia)
    # Crear variable para el día de la semana
    dia_semana = dia.weekday()
    print(dia_semana)
    # Diccionario de días
    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}
    # Decir el día de la semana
    hablar(f"Hoy es {calendario[dia_semana]}, {dia.today()}")

# Informar que hora es
def pedir_hora():
    """Informar que hora es"""
    # Crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f"Son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    print(hora)
    # Decir la hora
    hablar(hora)

# Saludo inicial
def saludo_inicial():
    """Saludo Inicial"""
    # Crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"
    # Decir el saludo
    hablar(f"{momento}, soy Sabina, tu asistente personal. Por favor, dime en que te puedo ayudar")

# Función Central del Asistente
def pedir_cosas():
    """Función Central del Asistente"""
    # Activar saludo inicial
    saludo_inicial()
    # Variable de corte
    comenzar = True
    # Loop Central
    while comenzar:
        # Activar el micrófono y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()
        if "abrir youtube" in pedido:
            hablar("Con gusto, estoy abriendo YouTube")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "abrir navegador" in pedido:
            hablar("Claro, estoy en eso")
            webbrowser.open("https://www.google.com")
            continue
        elif "qué día es hoy" in pedido:
            pedir_dia()
            continue
        elif "qué hora es" in pedido:
            pedir_hora()
            continue
        elif "busca en wikipedia" in pedido:
            hablar("Buscando en Wikipedia")
            pedido = pedido.replace("busca en wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("Wikipedia dice lo siguiente:")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("Ya estoy en eso")
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("Ésto es lo que he encontrado")
            continue
        elif "reproducir" in pedido:
            hablar("Buena idea, ya comienzo a reproducirlo")
            pedido = pedido.replace("reproducir", "")
            pywhatkit.playonyt(pedido)
            continue
        elif "broma" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {"apple": "APPL",
                       "amazon": "AMZN",
                       "google": "GOOGL"}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info["regularMarketPreviousClose"]
                hablar(f"La encontré, el precio de {accion} es de {precio_actual}")
                continue
            except AssertionError:
                hablar("Lo siento, no he encontrado lo que me pediste")
                continue
        elif "adiós" in pedido:
            hablar("Me voy a descansar, cualquier cosa me avisas")
            break

pedir_cosas()
