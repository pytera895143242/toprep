from aiogram import types
from misc import dp,bot
import sqlite3
from .sqlit import reg_user

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    reg_user(message.chat.id,'123')

    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='🥤НАЧАТЬ СМОТРЕТЬ🥤', callback_data= f'start_watch_')
    markup.add(bat_a)
    await bot.send_message(message.chat.id, text= f'🥤Все новинки фильмов доступны на нашем <b>основном канале.</b> \n'
                                            '\n'
                                            '📲Приятного просмотра 👇👇👇',parse_mode='html',reply_markup=markup)

