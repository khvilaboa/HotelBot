# HotelBot
ChatBot que pretende gestionar la reserva de habitaciones en un hotel. Entre los principales factores a tratar se encuentran:
- Fechas de entrada y salida al hotel.
- Tipos de habitación (pudiendo mostrar imágenes de las mismas).
- Servicios:
  - Tipo de pensión (desayuno, medio pension, pensión completa).
  - Información de "Como llegar".
  - Información de tiempo atmosférico.
- Posibilidad de enviar correos electrónicos para confirmar la reserva.
- Valoración de la experiencia.

## Instalación
HotelBot tiene las siguientes dependencias:

**Python Telegram API**, para crear el bot de Telegram.

```   pip install python-telegram-bot```

**NLTK**: para analizar lenguaje natural.

```   pip install nltk```

**Langdetect, langid y textblob**: para la detección del idioma.

```   pip install Langdetect langid textblob```
