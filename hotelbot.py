#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
updater = Updater(token='344919668:AAFvtg7WYYvxT9d8msQAu6cvbsmggKwyDEk')  # @DASIHotelBot

dispatcher = updater.dispatcher

# Default command (executed on bot init)
def start(bot, update):
	update.message.reply_text("Buenaaaas. Una habitacion?")

# To handle text (text that doesn't start with '/')
def text(bot, update):
	# Add intelligence here
	print update
	update.message.reply_text("Mi no entender :(")

# To handle unknown commands
def unknown(bot, update):
	#print update  # Uncomment to view message info
	update.message.reply_text("Comando no reconocido.")

# To handle images
def images(bot, update):
	update.message.reply_text("Eso... es una imagen.")

# Example of in-line keyboard use
def room_types(bot, update):
	#rooms_keyboard = [['Individual', 'Doble', 'Suite']]
	keyboard = [[InlineKeyboardButton("Individual", callback_data='Individual')], \
                [InlineKeyboardButton("Doble", callback_data='Doble')], \
                [InlineKeyboardButton("Suite", callback_data='Suite')]]
					
	rooms_markup = InlineKeyboardMarkup(keyboard) #, one_time_keyboard=True
				
	update.message.reply_text("Tenemos los siguientes tipos de habitación. Elije una, por favor.", \
								reply_markup=rooms_markup)
	
# Example of in-line keyboard use
def keyboard_press(bot, update):
	query = update.callback_query
	
	# To modify the keyboard message ("una habitación" if query.data != "Suite" else "", query.data)
	bot.editMessageText(text="Has seleccionado: %s" % query.data,
						chat_id=query.message.chat_id,
						message_id=query.message.message_id)
	
# Handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('roomtypes', room_types))
dispatcher.add_handler(MessageHandler(Filters.text, text))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))
dispatcher.add_handler(MessageHandler(Filters.photo, images))
updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_press))  # To handle keyboard press


updater.start_polling()  # Starts the bot