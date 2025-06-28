import random
import requests
import os
from datetime import datetime
import pytz

# --- CONFIGURACIÓN ---
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# Imprimir valores para depuración (solo primeros caracteres por seguridad)
if not BOT_TOKEN or not CHAT_ID:
    print("❌ Error: BOT_TOKEN o CHAT_ID no configurados")
    exit(1)  # Fuerza el fallo del workflow si falta algo
print(f"Token recibido: {BOT_TOKEN[:5]}... (parcial)")
print(f"Chat ID recibido: {CHAT_ID}")

# --- LISTA DE MENSAJES MOTIVACIONALES POR CATEGORÍA ---
mensajes_por_categoria = {
    "salir_exponer": [
        "El mundo te espera. ¡Hoy es un día perfecto para explorar un nuevo lugar o actividad en Lima!",
        "Las conexiones no nacen en la inactividad. ¿Qué pequeño paso social darás hoy para expandir tu círculo?",
        "Tu vida social es un músculo. ¡Cada interacción es un entrenamiento! Sal y muestra tu luz.",
        "Hoy, la aventura te llama. Abre una app de citas o busca un evento que te interese. ¡La acción es clave!",
        "No hay camino sin el primer paso. ¿Con quién podrías iniciar una conversación hoy, por pequeña que sea?"
    ],
    "confianza_comunicacion": [
        "Tu voz es única. ¡Permite que se escuche! Practica una conversación hoy, por el simple placer de conectar.",
        "La confianza no es ausencia de miedo, es acción a pesar de él. ¿Qué acto de confianza darás hoy?",
        "Escuchar es un superpoder. Hoy, enfócate en entender antes de ser entendido. ¡La empatía construye puentes!",
        "El rechazo es una flecha que apunta a la siguiente oportunidad. ¡Levántate, aprende y sigue adelante!",
        "Tu autenticidad es tu mayor atractivo. Sé tú mismo hoy y mira cómo las conexiones fluyen."
    ],
    "evitar_saboteadores": [
        "Cambia la inactividad por la oportunidad. ¿Dónde está tu próxima aventura social hoy?",
        "El miedo se disuelve con la acción. Enfrenta un pequeño temor social y siente cómo tu fuerza crece.",
        "La energía sexual es poderosa. Dirígela hacia interacciones reales y conexiones significativas. ¡El mundo te espera!",
        "Tu valía no se mide por encuentros pasados. Mira hacia adelante y construye las experiencias que deseas.",
        "Deja que la realidad supere la fantasía. Hoy, enfoca tu energía en el emocionante mundo de las interacciones humanas."
    ],
    "autocuidado_crecimiento": [
        "Eres tu proyecto más importante. ¿Qué harás hoy para nutrir tu mente, cuerpo o espíritu?",
        "Invierte en ti. Cada esfuerzo en tu salud y bienestar te acerca a la persona magnética que quieres ser.",
        "Tu energía es contagiosa. Aliméntala con buenos hábitos. ¿Qué decisión saludable tomarás hoy?",
        "La vida es más rica con pasiones. Dedica tiempo hoy a algo que amas y que te haga sentir vivo.",
        "Sé tu mejor versión, por ti y para ti. El atractivo genuino nace del autorespeto y el crecimiento."
    ],
    "inspirador_general": [
        "Cada día es una nueva oportunidad para construir la vida social que sueñas. ¡Empieza ahora!",
        "No necesitas perfección, necesitas progresión. Hoy da un paso, aunque sea pequeño.",
        "Tus habilidades sociales son músculos: cuanto más los usas, más fuertes se vuelven.",
        "Confía en que cada interacción te acerca a alguien especial. ¡La conexión puede estar hoy frente a ti!",
        "La experiencia más enriquecedora empieza con una sola palabra: Hola."
    ]
}

# --- FUNCIÓN PARA ENVIAR MENSAJE ---
def enviar_mensaje_telegram(mensaje):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Lanza excepción si falla
        print(f"Respuesta de Telegram: {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al enviar mensaje: {e}")
        exit(1)  # Fuerza el fallo del workflow si hay un error de red

# --- FUNCIÓN PARA SELECCIONAR MENSAJE SEGÚN LA HORA ---
def seleccionar_mensaje_por_hora():
    lima_tz = pytz.timezone('America/Lima')
    hora_actual = datetime.now(lima_tz).hour
    print(f"Hora actual en Lima: {hora_actual}:00")
    
    if hora_actual == 8:  # 8:00 AM
        categoria = "salir_exponer"
    elif hora_actual == 10:  # 10:00 AM
        categoria = "confianza_comunicacion"
    elif hora_actual == 12:  # 12:45 PM (aproximado al cron)
        categoria = "inspirador_general"
    else:
        categoria = "inspirador_general"
    
    mensaje = random.choice(mensajes_por_categoria[categoria])
    print(f"Mensaje seleccionado: {mensaje}")
    return mensaje

# --- PROGRAMA PRINCIPAL ---
def main():
    mensaje = seleccionar_mensaje_por_hora()
    resultado = enviar_mensaje_telegram(mensaje)
    
    if resultado and resultado.get('ok'):
        print(f"✅ Mensaje enviado exitosamente: {mensaje}")
    else:
        print(f"❌ Error al enviar mensaje: {resultado or 'No response from Telegram'}")
        exit(1)

if __name__ == "__main__":
    main()
