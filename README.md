# 🚀 Crea tu bot de alertas de precios para acciones y criptomonedas
Este repositorio contiene el código para que puedas crear tu propio bot de Telegram que te notificará sobre cambios en los precios de criptomonedas y acciones. Se ha desarrollado utilizando la biblioteca python-telegram-bot.

Espero que te sea útil y puedas sacarle el máximo provecho.

## ⚙️ Configuración
1️⃣ Clona este repositorio en tu ordenador.

2️⃣ Instala las dependencias utilizando el siguiente comando:

```bash
pip install -r requirements.txt
```
3️⃣ Crea tu bot en Telegram a través de BotFather y obtén su token.

4️⃣ Reemplaza 'TU_TOKEN_AQUI' en la función main() de los archivos crypto_bot.py y telegram_bot.py con el token proporcionado por BotFather.

5️⃣ Ejecuta el bot con uno de los siguientes comandos según el bot que quieras usar:

```bash
python crypto_bot.py   # Para el bot de criptomonedas  
python telegram_bot.py # Para el bot de acciones  
```
## ⚙️ Funcionalidades  

Este bot te permite monitorear el precio de **acciones y criptomonedas** y recibir alertas cuando alcancen un valor específico.  

### 📌 Comandos disponibles  

- **`/start`** → Inicia el bot y muestra un mensaje de bienvenida con instrucciones.  
- **`/misdatos`** → Muestra la criptomoneda o acción que estás monitoreando y el precio de alerta configurado.  
- **`/help`** → Explica cómo funciona el bot y cómo configurar alertas.  

### 🚀 ¿Cómo usarlo?  
1️⃣ Envía el **nombre o ticker** de la criptomoneda o acción que quieres monitorear (Ejemplo: `Bitcoin` o `AAPL` para Apple).  

2️⃣ Envía el **precio objetivo** al que deseas recibir una alerta (Ejemplo: `45000` para Bitcoin o `150` para Apple).  

3️⃣ ¡Listo! Cuando el precio alcance tu objetivo, recibirás una **notificación automática**.  

📊 **El bot consulta los precios en tiempo real usando Yahoo Finance para acciones y CoinGecko para criptomonedas.**
