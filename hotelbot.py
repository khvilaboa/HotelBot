#!/usr/bin/env python
# -*- coding: utf8 -*-

# Mail for future use: dasihotelbot@gmail.com / 3m0j1Lun4

import traceback

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from agents import HotelAgent, InsultsAgent, UserInput

updater = Updater(token='344919668:AAFvtg7WYYvxT9d8msQAu6cvbsmggKwyDEk')  # @DASIHotelBot
dispatcher = updater.dispatcher

agents = [HotelAgent(), InsultsAgent()]


# Default command (executed on bot init)
def start(bot, update):
    update.message.reply_text("Buenaaaas. Una habitacion?")


# To handle text (that doesn't start with '/')
def text(bot, update):
    text = update.message.text
    print("\nReceived: %s" % text)
    try:
        input = UserInput(text)
        response = max([agent.evaluate(input) for agent in agents])[1]
        print("Response: " + response)
        update.message.reply_text(response)
    except Exception as e:
        traceback.print_exc()
        print(e)


# To handle unknown commands
def unknown(bot, update):
    # print update  # Uncomment to view message info
    update.message.reply_text("Comando no reconocido.")


# To handle images
def images(bot, update):
    update.message.reply_text("Eso... es una imagen.")


# Example of in-line keyboard use
def room_types(bot, update):
    # rooms_keyboard = [['Individual', 'Doble', 'Suite']]
    keyboard = [[InlineKeyboardButton("Individual", callback_data='Individual')], \
                [InlineKeyboardButton("Doble", callback_data='Doble')], \
                [InlineKeyboardButton("Suite", callback_data='Suite')]]

    rooms_markup = InlineKeyboardMarkup(keyboard)  # , one_time_keyboard=True

    update.message.reply_text("Tenemos los siguientes tipos de habitación. Elije una, por favor.", \
                              reply_markup=rooms_markup)

def pension_types(bot, update):
    # rooms_keyboard = [['Individual', 'Doble', 'Suite']]
    keyboard = [[InlineKeyboardButton("Solo desayuno", callback_data='desayuno')], \
                [InlineKeyboardButton("Media pensión", callback_data='media')], \
                [InlineKeyboardButton("Pensión completa", callback_data='completa')]]

    rooms_markup = InlineKeyboardMarkup(keyboard)  # , one_time_keyboard=True

    update.message.reply_text("Qué tipo de pensión desea?. Elije una, por favor.", \
                              reply_markup=rooms_markup)

def user_valoration(bot, update):
    keyboard = [[InlineKeyboardButton("\u2B50", callback_data='deficiente')], \
                [InlineKeyboardButton("\u2B50\u2B50", callback_data='baja')], \
                [InlineKeyboardButton("\u2B50\u2B50\u2B50", callback_data='normal')], \
                [InlineKeyboardButton("\u2B50\u2B50\u2B50\u2B50", callback_data='buena')], \
                [InlineKeyboardButton("\u2B50\u2B50\u2B50\u2B50\u2B50", callback_data='muy buena')]]

    valoration_markup = InlineKeyboardMarkup(keyboard)  # , one_time_keyboard=True

    update.message.reply_text("Gracias por confiar en nosotros. Antes de que se marche, ¿podría valorar su experiencia conmigo?", \
                              reply_markup=valoration_markup)
    
    

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
dispatcher.add_handler(CommandHandler('pensiontypes', pension_types))
dispatcher.add_handler(CommandHandler('uservaloration', user_valoration))
dispatcher.add_handler(MessageHandler(Filters.text, text))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))
dispatcher.add_handler(MessageHandler(Filters.photo, images))
updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_press))  # To handle keyboard press

updater.start_polling()  # Starts the bot
