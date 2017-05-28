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

Se recomienda utilizar Python 2 para ejecutar el bot.

## Instalación
HotelBot tiene las siguientes dependencias:

**Python Telegram API**, para crear el bot de Telegram.

```   pip install python-telegram-bot```

**NLTK**: para analizar lenguaje natural.

```   pip install nltk```

**Langdetect, langid y textblob**: para la detección del idioma.

```   pip install Langdetect langid textblob```

**pyowm**: para el pronóstico meteorológico.

```   pip install pyowm```

**googlemaps**: para las indicaciones de cómo llegar al hotel.

```   pip install googlemaps```

**Intellect**: sistema de reglas.

```pip install http://antlr3.org/download/Python/antlr_python_runtime-3.1.3.tar.gz```

```pip install Intellect```

**PyMongo**: para la comunicación de la base de datos. Antes de ejecutar HotelBot será necesario el despliegue de un servidor de Mongo, para el almacenamiento persistente de la información generada por el mismo (en el puerto por defecto).

```pip install pymongo```

**APScheduler**: para la gestión de tareas asíncronas (comunicación con el usuario sin interacción previa).

```pip install apscheduler```

Todas estas dependencias además están recogidas en el fichero **requirements.txt**. Para obtener todas las dependencias
sin necesidad de escribirlas a mano una a una, basta con ejecutar el siguiente comando:

```   pip install -r requirements.txt```

## Autores
Estos son los autores de este proyecto:
- Kevin Henares ([@khvilaboa](https://github.com/khvilaboa))
- Iván Martínez ([@iMartinezMateu](https://github.com/iMartinezMateu))
- Fernando Suárez ([@fersj](https://github.com/fersj))
- Christian Álvarez ([@chalvare](https://github.com/chalvare))
- Kevin Arboleda ([@kevinarb](https://github.com/kevinarb))
- Diego Monjas ([@dmonjas](https://github.com/dmonjas))

