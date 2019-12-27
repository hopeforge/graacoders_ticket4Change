"""
Baseano no template open-source fornecido pela propria documentação do TeleBot API

"""
import requests
import time
import os
import telebot
from telebot import types

from directory import Directory
from exporter import Exporter
from image_decoder import ImageDecoder

TOKEN = '1023504391:AAEodSKmzb17E7Mdf7ZBaka-lvMGCAYfVJQ'

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start'       : 'Inicia a utilização do bot',
    'help'        : 'Fornece infomações sobre os comandos disponíveis',
    'cupom'       : 'Envia uma foto de uma nota fiscal paulista como doação'
}

# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("Olá, nos ainda não nos conhecemos, use o comando \"/start\" para começar")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
        elif m.content_type == 'photo':
            cid = m.chat.id
            bot.send_message(cid, "Por favor envie um documento valido")
        elif m.content_type == 'document':
            cid = m.chat.id
            bot.send_message(cid, "Seu documento está sendo analisado, por favor aguarde ...")
            photo = m.document.file_id
            arq = bot.get_file(photo)
            downloaded_file = bot.download_file(arq.file_path)
            
            with open('C:\\repositorio\\input\\figura_1.jpeg', 'wb') as new_file:
                new_file.write(downloaded_file)
            
            directory = Directory()
            path_in = 'C:\\repositorio\\input\\'
            path_out = 'C:\\repositorio\\output\\'
            image_files = directory.get_images(path_in)

            decoder = ImageDecoder()

            exporter = Exporter()

            for image in image_files:
                decoded_image = decoder.decode_qr_code(image)
                list_to_export = decoder.get_decoded_value(decoded_image)
                if bool(list_to_export):
                    exporter.write_csv(path_out, 'cupom_fiscal', list_to_export)

            bot.send_message(cid, "Obrigado por enviar seu cupom!")

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener

# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "Bem vindo ao chatbot do GRAACC")
        bot.send_message(cid, "Estamos registrando você como novo usuário ...")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "Olá! Que bom que voltou, sentimos sua falta")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "A seguinte lista de comandos está disponível: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


# chat_action example (not a good one...)
@bot.message_handler(commands=['cupom'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Doe para salvar vidas... sua doação faz a diferença")
    bot.send_message(cid, "Acesse o site do GRAACC e faça a diferença\nPara doar seu cupom fiscal envie uma foto")

@bot.message_handler(func=lambda message: message.content_type == "photo")
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Obrigado por enviar seu cupom!")

# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "oi" or message.text == 'Oi' )
def command_text_hi(m):
    bot.send_message(m.chat.id, "Oi! Bem vindo de volta, em que posso ajudar?")

@bot.message_handler(func=lambda message: message.text == "doar" or message.text == "doação" )
def mensagem_doacao(m):
    bot.send_message(m.chat.id, "Para doar você pode acessar nosso site: https://graacc.org.br/doar/")
    bot.send_message(m.chat.id, "Você também pode doar sua nota fiscal paulista utilizando o comando \"/cupom\"")

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "Não consigo te entender \"" + m.text + "\"\nTente ajuda em /help")

bot.polling()