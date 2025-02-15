from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes, CallbackContext
import yfinance as yf

# Función para verificar si el ticker es válido
user_data = {}


def es_accion_valida(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info.get("currentPrice")
        if current_price == None:
            return False
        return "longName" in info and info["longName"] is not None
    except Exception:
        return False


async def start(update, context):
    """ Mensaje de bienvenida """
    texto = """Este bot te ayuda a monitorear el precio de una acción y te avisará cuando llegue al valor que indiques.

    🔹 Instrucciones:
    1️⃣ Envía el ticker de la acción que quieres monitorear (Ejemplo: AAPL para Apple).
    2️⃣ Envía el precio al cual deseas recibir una alerta (Ejemplo: 150).

    Cuando el precio de la acción alcance el valor que indicaste, recibirás una notificación."""
    await update.message.reply_text(texto)


async def recibir_ticker_precio(update, context):
    """ Recibe el ticker y el precio del usuario """
    texto = update.message.text

    if texto.isdigit() or texto.replace(".", "", 1).isdigit():
        user_id = update.message.from_user.id

        # Comprobamos que estamos esperando un precio
        if context.user_data.get('estado') == 'esperando_precio':
            print("Estoy dentro")
            try:
                ticker = context.user_data.get("ticker", None)
                if ticker is None:
                    await update.message.reply_text("⚠️ Primero dime qué *ticker* quieres monitorear.")
                    return

                token = yf.Ticker(ticker)

                info_token = token.info
                try:
                    current_price = info_token.get("currentPrice")
                except Exception as e:
                    print(f"Error obteniendo el precio: {e}")
                    exit()

                # Convertimos a número
                precio_objetivo = float(update.message.text)
                user_data[user_id]["precio"] = precio_objetivo
                if (precio_objetivo > current_price):
                    print("El precio que busca es mayor")
                    user_data[user_id]["direc"] = "suba"
                else:
                    print("El precio que busca es menor")
                    user_data[user_id]["direc"] = "baje"
                # Obtenemos el ticker que ya guardamos
                ticker = context.user_data['ticker']

                # Guardamos el precio objetivo
                context.user_data['precio'] = precio_objetivo

                await update.message.reply_text(
                    f"📌 Monitoreando {ticker} y te avisaré cuando llegue a {precio_objetivo} 💰"
                )
                # Cambiamos el estado a 'listo', ya no esperamos más
                context.user_data['estado'] = 'listo'
            except ValueError:
                await update.message.reply_text("❌ Eso no parece un número válido. Ingresa solo el precio.")
        else:
            await update.message.reply_text("⚠️ Primero dime qué *ticker* quieres monitorear.")
    else:
        user_id = update.message.from_user.id
        ticker = update.message.text.upper()

        token = yf.Ticker(ticker)

        info_token = token.info
        try:
            current_price = info_token.get("currentPrice")
        except Exception as e:
            print(f"Error obteniendo el precio: {e}")
            exit()

        if es_accion_valida(ticker):
            # Guardamos el ticker en user_data y cambiamos el estado
            user_data[user_id] = {"ticker": ticker}
            context.user_data['ticker'] = ticker
            # Cambiamos el estado
            context.user_data['estado'] = 'esperando_precio'
            await update.message.reply_text(f"✅ {ticker} es una acción válida y su precio es {current_price}. ¿A qué precio quieres que te avise?")
        else:
            await update.message.reply_text(f"❌ {ticker} no es una acción válida. Intenta con otro.")


async def mostrar_datos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Muestra los datos almacenados para el usuario """
    user_id = update.message.from_user.id
    if user_id in user_data and "ticker" in user_data[user_id] and "precio" in user_data[user_id]:
        ticker = user_data[user_id]["ticker"]
        precio = user_data[user_id]["precio"]
        direcion = user_data[user_id]["direc"]
        await update.message.reply_text(f"📊 Estás monitoreando {ticker} con un objetivo de ${precio} y estas esperando que el precio {direcion}")
    else:
        await update.message.reply_text("⚠️ No tienes ninguna acción en monitoreo aún.")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Muestra las caracteristicas del boy """
    texto = """📌 Cómo usar el bot 📌

    Este bot te ayuda a monitorear el precio de una acción y te avisará cuando llegue al valor que indiques.

    🔹 Instrucciones:
    1️⃣ Envía el ticker de la acción que quieres monitorear (Ejemplo: AAPL para Apple).
    2️⃣ Envía el precio al cual deseas recibir una alerta (Ejemplo: 150).

    Cuando el precio de la acción alcance el valor que indicaste, recibirás una notificación.

    🔹 Comandos disponibles:
    📊 /misdatos → Muestra qué acción estás monitoreando y el precio de alerta configurado.

    Si tienes dudas, ¡envíame un mensaje! 🚀"""
    await update.message.reply_text(texto)


async def verificar_precio(context: CallbackContext):

    if not user_data:
        print("La variable está vacía, no hace falta comprobar nada.")
    else:
        print("Estoy comprobando")
        # Convertimos las claves a una lista para evitar modificar el diccionario mientras se itera
        for user_id in list(user_data.keys()):
            data = user_data[user_id]

            # Verificamos si todos los campos necesarios están presentes
            if all(key in data for key in ["ticker", "precio", "direc"]):
                ticker = data["ticker"]
                target_price = data["precio"]
                direction = data["direc"]

                stock = yf.Ticker(ticker)
                info = stock.info
                current_price = info.get("currentPrice")

                if direction == "suba" and current_price >= target_price:
                    await context.bot.send_message(user_id, f"📉 El precio de {ticker} ha subido y alcanzó tu valor objetivo de {target_price}. El precio actual es {current_price}.")
                    del user_data[user_id]
                elif direction == "baje" and current_price <= target_price:
                    await context.bot.send_message(user_id, f"📈 El precio de {ticker} ha bajado y alcanzó tu valor objetivo de {target_price}. El precio actual es {current_price}.")
                    del user_data[user_id]
                else:
                    print("No se ha llegado al precio objetivo para notificacion")
                # Eliminar la acción de monitoreo si ya alcanzó el precio

            else:
                # Si falta algún campo, no hacer nada y continuar con la siguiente iteración
                print(
                    f"Faltan campos para el usuario {user_id}, no se realiza comprobación.")


def main():
    """ Configuración del bot """
    app = Application.builder().token(
        "7697013034:AAE7OCXTPo0FYbSbgWpGqC-GBO7cOSjV9yY").build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("misdatos", mostrar_datos))
    app.add_handler(CommandHandler("help", help))
    # Para manejar mensajes
    app.add_handler(MessageHandler(
        ~filters.COMMAND, recibir_ticker_precio))  # Captura tickers

    print("🤖 Bot en marcha...")

    # Configurar el JobQueue para ejecutar la verificación del precio cada minuto
    job_queue = app.job_queue
    # Verificar cada 60 segundos
    job_queue.run_repeating(verificar_precio, interval=60, first=10)

    app.run_polling()


if __name__ == "__main__":
    main()
