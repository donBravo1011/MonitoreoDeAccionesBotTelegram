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
## 📦 Dependencias
Asegúrate de instalar los siguientes paquetes antes de ejecutar el bot:

```bash
pip install python-telegram-bot
pip install python-telegram-bot[job-queue]
pip install yfinance
pip install pycoingecko
```