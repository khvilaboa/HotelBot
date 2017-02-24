from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
updater = Updater(token='344919668:AAFvtg7WYYvxT9d8msQAu6cvbsmggKwyDEk')  # @DASIHotelBot

dispatcher = updater.dispatcher

# Default command (executed on bot init)
def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Buenaaaas. Una habitacion?")

# To handle text (text that doesn't start with '/')
def text(bot, update):
	# Add intelligence here
	print update
	bot.sendMessage(chat_id=update.message.chat_id, text="Mi no entender :(")

# To handle unknown commands
def unknown(bot, update):
	#print update  # Uncomment to view message info
	bot.sendMessage(chat_id=update.message.chat_id, text="Comando no reconocido.")

# Handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text, text))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()  # Starts the bot