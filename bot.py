from telebot import TeleBot, types

bot = TeleBot(token='7465379572:AAFKE52yohq4jsoyNlyXQ-UELfH2oEnCJCI')

@bot.message_handler(commands=['start'])
def listen(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Перейти', web_app=types.WebAppInfo('https://cepbep4-airvapebot-3c83.twc1.net')))
    bot.send_message(chat_id=message.chat.id, text='Добро пожаловать!', 
                    reply_markup=kb)

bot.infinity_polling()