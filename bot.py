from telebot import TeleBot, types
from requests import post, get
from dbcontrol import base_add

bot = TeleBot(token='7465379572:AAFKE52yohq4jsoyNlyXQ-UELfH2oEnCJCI')
HOST = 'https://cepbep4-airvapebot-b471.twc1.net'

def register_new_user(uid,username):
    base_add('user',{
        'balance':5,
        'case_info':{},
        'chat_id':uid,
        'id':0,
        'username':username
    })
    
def get_user(uid):
    rq = get(f'{HOST}/api/user?chat_id={uid}')
    print(rq.text)

@bot.message_handler(commands=['start'])
def listen(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Перейти', web_app=types.WebAppInfo('https://cepbep4-airvapebot-b471.twc1.net')))
    bot.send_message(chat_id=message.chat.id, text='Добро пожаловать!', 
                    reply_markup=kb)
    register_new_user(message.chat.id, message.from_user.username)
    #get_user(0)

bot.infinity_polling()
