#!/usr/bin/env python
# -*- coding: utf8 -*-

# Mail for future use: dasihotelbot@gmail.com / 3m0j1Lun4
# API key for weather service: 86b4bc5747efd019c9d6bf0da2c84813
import pdb

import traceback

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler
from agents import HotelAgent, InsultsAgent, LanguagesAgent
from facts import Response
from resources import UserInput, DBHandler
from utils.directions import Directions

updater = Updater(token='344919668:AAFvtg7WYYvxT9d8msQAu6cvbsmggKwyDEk')  # @DASIHotelBot
dispatcher = updater.dispatcher

agents = {"insults": InsultsAgent(), "languages": LanguagesAgent()}  # HotelAgent()
chat_ids = {}

TIME_WARN_MIN = 5
TIME_ERASE_MIN = 10

scheduler = BackgroundScheduler()
scheduler.start()

# ------------------------------------------------------------------------------

def check_agent(username):
    if username not in agents:
        subscribe(username)

# Register a user specific agent
def subscribe(username):
    agents[username] = HotelAgent(username)

def unsubscribe(username):
    del agents[username]

def lookup_user(chat_id):
    for user, ci in chat_ids.iteritems():
        if ci == chat_id:
            return user
    return None

def c_warn_user(bot, username):
    scheduler.remove_job(username)
    chat_id = chat_ids[username]
    bot.sendMessage(chat_id=chat_id, text="Ha pasado un tiempo desde el último mensaje... si pasan %d minutos más se reiniciará la sesión" % TIME_ERASE_MIN)
    scheduler.add_job(c_remove_chat, 'interval', minutes=TIME_ERASE_MIN, args=(bot, username), id=username, replace_existing=True)

def c_remove_chat(bot, username):
    scheduler.remove_job(username)

    chat_id = chat_ids[username]
    bot.sendMessage(chat_id=chat_id, text="Sesión reiniciada")

    unsubscribe(username)
    del chat_ids[username]

# ------------------------------------------------------------------------------
# Default command (executed on bot init)
def start(bot, update):
    update.message.reply_text("Buenaaaas. Una habitacion?")


# To handle text (that doesn't start with '/')
def text(bot, update):
    text = update.message.text
    # pdb.set_trace()
    username = update.message.from_user.username
    check_agent(username)

    if username not in chat_ids:
        chat_ids[username] = update.message.chat_id

    print("\nReceived: %s" % text)
    try:
        input = UserInput(text)
        suitable_agents = (agents["insults"], agents[username], agents["languages"])
        response = max([agent.evaluate(input) for agent in suitable_agents])[1]
        print("Response: ", response.msg)
        for msg in response.msg:
            update.message.reply_text(msg)

        # Keyboards
        if response.keyboard == Response.KEYBOARD_ROOM_TYPES:
            room_types(bot, update)
        elif response.keyboard == Response.KEYBOARD_PENSION_TYPES:
            pension_types(bot, update)

        # Actions
        if response.action == Response.ACTION_SHOW_ROOMS:
            images(bot, update)
    except Exception as e:
        traceback.print_exc()
        print(e)

    scheduler.add_job(c_warn_user, 'interval', minutes=TIME_WARN_MIN, args=(bot, username), id=username, replace_existing=True)



# To handle unknown commands
def unknown(bot, update):
    # print update  # Uncomment to view message info
    update.message.reply_text("Comando no reconocido.")


# To handle images
def images(bot, update):
    db = DBHandler()
    chat_id = update.message.chat_id
    update.message.reply_text("Habitación individual (%d EUR/noche)" % db.price(DBHandler.ROOM_INDIVIDUAL))
    bot.sendPhoto(chat_id=chat_id, photo=open("images/individual.jpg", 'rb'))
    update.message.reply_text("Habitación doble (%d EUR/noche)" % db.price(DBHandler.ROOM_DOUBLE))
    bot.sendPhoto(chat_id=chat_id, photo=open("images/doble.jpg", 'rb'))
    update.message.reply_text("Suite (%d EUR/noche)" % db.price(DBHandler.ROOM_SUITE))
    bot.sendPhoto(chat_id=chat_id, photo=open("images/suite.jpg", 'rb'))


# To handle locations
def location(bot, update):
    db = DBHandler()
    hotel_loc = db.location()
    loc = update.message.location

    update.message.reply_text(
        "Puedes consultar la ruta desde la localización enviada hasta el hotel en el siguiente enlace:")
    update.message.reply_text(Directions.route_url(loc.latitude, loc.longitude, hotel_loc[0], hotel_loc[1]))


# Example of in-line keyboard use
def room_types(bot, update):
    db = DBHandler()
    # pdb.set_trace()
    keyboard = [[InlineKeyboardButton("Individual (%d EUR/noche)" % db.price(DBHandler.ROOM_INDIVIDUAL),
                                      callback_data='individual')], \
                [InlineKeyboardButton("Doble (%d EUR/noche)" % db.price(DBHandler.ROOM_DOUBLE), callback_data='doble')], \
                [InlineKeyboardButton("Suite (%d EUR/noche)" % db.price(DBHandler.ROOM_SUITE), callback_data='suite')]]

    rooms_markup = InlineKeyboardMarkup(keyboard)  # , one_time_keyboard=True

    update.message.reply_text("Tenemos los siguientes tipos:", \
                              reply_markup=rooms_markup)


def pension_types(bot, update):
    db = DBHandler()
    # pdb.set_trace()
    keyboard = [[InlineKeyboardButton("Completa (%d EUR/dia)" % db.price_pension(DBHandler.PENSION_FULL),
                                      callback_data='completa')], \
                [InlineKeyboardButton("Parcial (%d EUR/dia)" % db.price_pension(DBHandler.PENSION_HALF),
                                      callback_data='parcial')], \
                [InlineKeyboardButton("Desayuno (%d EUR/dia)" % db.price_pension(DBHandler.PENSION_BREAKFAST),
                                      callback_data='desayuno')]]

    rooms_markup = InlineKeyboardMarkup(keyboard)  # , one_time_keyboard=True

    update.message.reply_text("Tenemos los siguientes tipos:", \
                              reply_markup=rooms_markup)


# Example of in-line keyboard use
def keyboard_press(bot, update):
    query = update.callback_query

    # To modify the keyboard message ("una habitación" if query.data != "Suite" else "", query.data)
    bot.editMessageText(text="Has seleccionado: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

    username = lookup_user(query.message.chat_id)

    if(query.data in ('individual', 'doble', 'suite')):
        agents[username].intellect.set_room_type(query.data)
    elif(query.data in ('completa', 'parcial', 'desayuno')):
        agents[username].intellect.set_pension_type(query.data)

    msg = agents[username].intellect.next_question()
    if type(msg) is not list:
        bot.sendMessage(chat_id=query.message.chat_id, text=msg)
    else:
        for m in msg:
            bot.sendMessage(chat_id=query.message.chat_id, text=m)




# ------------------------------------------------------------------------------

# Handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('roomtypes', room_types))
dispatcher.add_handler(MessageHandler(Filters.text, text))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))
dispatcher.add_handler(MessageHandler(Filters.photo, images))
dispatcher.add_handler(MessageHandler(Filters.location, location))
updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_press))  # To handle keyboard press

updater.start_polling()  # Starts the bot
