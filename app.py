# i don't have time to translate comments
# sorry SkillFactory

import telebot
from extensions import *
import ownerconfig

bot = telebot.TeleBot(ownerconfig.tgb_token)


# always appears on /start and /help
@bot.message_handler(commands=['start', 'help'])
def start_help_message(message: telebot.types.Message):
    text = ("""Это - бот для перевода бумажных денег.\n\
Чтобы использовать бот, введите, через пробел и без скобок: \
<название желаемой валюты> <название используемой валюты> <кол-во желаемой валюты>.\n\
Введите "/values" для списка доступных валют. \n\
Введите "/help" чтобы снова вывести это сообщение. \n\
Информация о курсе валют извлечена из "CurrencyAPI", во время запуска этого бота. Перезапуск освежит эту информацию.""")
    bot.send_message(message.chat.id, text)


# "/values" displays currencies that can be used
@bot.message_handler(commands=['values'])
def currency_get_message(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in ownerconfig.uik:
        text = "\n".join((text, key))
    bot.send_message(message.chat.id, text)


# the main thing, responds to all text
@bot.message_handler(content_types=['text'])
def convert_message(message: telebot.types.Message):
    try:
        input_bd = message.text.split(" ")
        if len(input_bd) != 3:
            raise APIException("Ввод не соблюдает формату, попробуйте ещё раз.")
        base, quote, amount = input_bd
        text = "Цена - " + (str(CurInfoGet.get_price(base, quote, amount)))
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка:\n{e}")
    else:
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
