from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
import yfinance as yf

# Función para verificar si el ticker es válido


def es_accion_valida(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return "longName" in info and info["longName"] is not None
    except Exception:
        return False


async def start(update, context):
    """ Mensaje de bienvenida """
    await update.message.reply_text(
        "👋 ¡Bienvenido a *ElGallo*! 🐔📈\n\n"
        "Soy tu asistente de monitoreo de acciones. Dime el *ticker* de la acción que quieres seguir. 📊"
    )


async def recibir_ticker_precio(update, context):
    """ Recibe el ticker y el precio del usuario """
    texto = update.message.text

    if texto.isdigit() or texto.replace(".", "", 1).isdigit():
        user_id = update.message.from_user.id

        # Comprobamos que estamos esperando un precio
        if context.user_data.get('estado') == 'esperando_precio':
            print("Estoy dentro")
            try:
                # Convertimos a número
                precio_objetivo = float(update.message.text)
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
            context.user_data['ticker'] = ticker
            # Cambiamos el estado
            context.user_data['estado'] = 'esperando_precio'
            await update.message.reply_text(f"✅ {ticker} es una acción válida y su precio es {current_price}. ¿A qué precio quieres que te avise?")
        else:
            await update.message.reply_text(f"❌ {ticker} no es una acción válida. Intenta con otro.")


def main():
    """ Configuración del bot """
    app = Application.builder().token(
        "7697013034:AAE7OCXTPo0FYbSbgWpGqC-GBO7cOSjV9yY").build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, recibir_ticker_precio))  # Captura tickers

    print("🤖 Bot en marcha...")
    app.run_polling()


if __name__ == "__main__":
    main()
