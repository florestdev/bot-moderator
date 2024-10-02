import os
import time

try:
    import telebot # pip install pyTelegramBotAPI
    from telebot import TeleBot, types
    from g4f.client import Client # pip install g4f | pip install curl_cffi
    from g4f.Provider import Bing
except ImportError:
    input()
    os.system('pip install pyTelegramBotAPI')
    os.system('pip install g4f')
    os.system('pip install curl_cffi')

bot = TeleBot('введи токен')
banned_words = ['бананчики', 'домик', 'речка']
chat_id = -1002201845724
admins = [7455363246, 7389388731]

def check_message(text: str):
    for word in banned_words:
        if word in text.lower():
            return True
        else:
            pass
    return False

@bot.message_handler(content_types=['new_chat_members', 'left_chat_member'])
def join_and_leave(message: types.Message) -> None:
    if message.chat.type != 'supergroup':
        bot.send_message(message.chat.id, f'Бот не может работать не в супергруппе!')
    else:
        if message.chat.id != chat_id:
            bot.send_message(message.chat.id, f'Бот не может работать в чужих группах.')
            bot.leave_chat(message.chat.id)
        else:
            bot.delete_message(message.chat.id, message.id)
            chat_name = bot.get_chat(message.chat.id).title
            if message.new_chat_members:
                for member in message.new_chat_members:
                    bot.send_message(message.chat.id, f'{member.first_name}, приветствую! Добро пожаловать к нам в группу под названием "{chat_name}".\nСоветуем ознакомиться с нашими правилами!\nБлагодарим за визит!')
            else:
                bot.send_message(message.chat.id, f'{message.left_chat_member.first_name} покинул(а) группу.\nБлагодарим за проведенное время с нами!')

@bot.message_handler(content_types=['text'])
def moderate_group(message: types.Message) -> None:
    if message.chat.type != 'supergroup':
        bot.send_message(message.chat.id, f'Бот не может работать не в супергруппе!')
    else:
        if message.chat.id != chat_id:
            bot.send_message(message.chat.id, f'Бот не может работать в чужих группах.')
            bot.leave_chat(message.chat.id)
        else:
            if message.from_user.id in admins:
                pass
            else:
                if message.entities:
                    for entitie in message.entities:
                        if entitie.type in ['url', 'text_link']:
                            bot.delete_message(message.chat.id, message.id)
                            bot.send_message(message.chat.id, f'{message.from_user.first_name}, Вы были ограничены за отправку ссылки!')
                            bot.restrict_chat_member(message.chat.id, message.from_user.id, time.time()+3600, False, False, False, False, False, False, False, False)
                        else:
                            pass
                else:
                    if check_message(message.text):
                        bot.delete_message(message.chat.id, message.id)
                        bot.send_message(message.chat.id, f'{message.from_user.first_name}, Вы были ограничены за отправку запрещенного слова/выражения.')
                        bot.restrict_chat_member(message.chat.id, message.from_user.id, time.time()+7200, False, False, False, False, False, False, False, False)
                    else:
                        pass

bot.infinity_polling()