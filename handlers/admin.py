from aiogram import types
from misc import dp, bot
import sqlite3
from .sqlit import info_members,cheak_traf,obnovatrafika1,obnovalinka,obnovatrafika2,obnovatrafika3,obnovatrafika4,obnovatrafika5
from .callbak_data import obnovlenie
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 = 572493040 # ФЕДОР
ADMIN2 = 494588959

ADMIN_ID =[ADMIN_ID_1,ADMIN2]

class reg(StatesGroup):
    name = State()
    fname = State()

class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()


class del_user(StatesGroup):
    del_name = State()
    del_fname = State()

class reg_trafik(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_trafik2(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_trafik3(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_trafik4(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_trafik5(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_link(StatesGroup):
    traf1 = State()
    traf2 = State()

@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_e = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        bat_j = types.InlineKeyboardButton(text='Скачать базу данных', callback_data='baza')
        bat_setin = types.InlineKeyboardButton(text='Настройка трафика', callback_data='settings')

        markup.add(bat_a,bat_e)
        markup.add(bat_setin)
        markup.add(bat_j)
        await bot.send_message(message.chat.id,'Выполнен вход в админ панель',reply_markup=markup)


# НАСТРОЙКА ТРАФИКА
@dp.callback_query_handler(text='settings')
async def baza12(call: types.callback_query):
    markup_traf = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 1 КАНАЛ', callback_data='change_trafik')
    bat_a2 = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 2 КАНАЛ', callback_data='change_trafik2')
    bat_a3 = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 3 КАНАЛ', callback_data='change_trafik3')
    bat_a4 = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 4 КАНАЛ', callback_data='change_trafik4')
    bat_a5 = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 5 КАНАЛ', callback_data='change_trafik5')


    bat_b = types.InlineKeyboardButton(text='ИЗМЕНИТЬ ПОСЛЕДНЮЮ ССЫЛКУ⚙️', callback_data='change_link')
    bat_c = types.InlineKeyboardButton(text='ЗАКРЫТЬ', callback_data='otemena')

    markup_traf.add(bat_a)
    markup_traf.add(bat_a2)
    markup_traf.add(bat_a3)
    markup_traf.add(bat_a4)
    markup_traf.add(bat_a5)

    markup_traf.add(bat_b)
    markup_traf.add(bat_c)

    list = cheak_traf()
    await bot.send_message(call.message.chat.id, text=f'Список активных каналов на данный момент:\n\n'
                                                      f'1. {list[0]}\n'
                                                      f'2. {list[1]}\n'
                                                      f'3. {list[2]}\n'
                                                      f'4. {list[3]}\n'
                                                      f'5. {list[4]}\n\n'
                                                      f'Для изменения жми кнопку',parse_mode='html',reply_markup=markup_traf,disable_web_page_preview=True)

@dp.callback_query_handler(text='change_link') # Изменение ссылки
async def change_link(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)
    await bot.send_message(call.message.chat.id, text='Введите новую ссылку на конечный канал',reply_markup=markup)

    await reg_link.traf1.set()

@dp.message_handler(state=reg_link.traf1, content_types='text')
async def link_obnovlenie(message: types.Message, state: FSMContext):
    try:
        obnovalinka(message.text)
        await bot.send_message(chat_id=message.chat.id, text='Обновление успешно')
        await state.finish()

    except:
        await bot.send_message(chat_id=message.chat.id, text='Неудачно')
        await state.finish()



@dp.callback_query_handler(text='change_trafik') # Изменение каналов, на которые нужно подписаться
async def baza12342(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Отправь ссылку на новый, первый по счету канал\n',parse_mode='html',reply_markup=markup)
    await reg_trafik.traf1.set()

@dp.message_handler(state=reg_trafik.traf1, content_types='text')
async def traf_obnovlenie1(message: types.Message, state: FSMContext):
    await state.update_data(link_one = message.text)
    await bot.send_message(chat_id=message.chat.id, text=f'Теперь перешли мне любой пост из этого канала ({message.text})')
    await reg_trafik.traf2.set()



@dp.message_handler(state=reg_trafik.traf2, content_types=['text','photo','video'])
async def traf_obnovlenie(message: types.Message, state: FSMContext):
    link = await state.get_data()

    link_one = link['link_one'] #Ссылка на канал
    id_channel1 = (message.forward_from_chat.id) #ID канала

    try:
        obnovatrafika1(link_one, id_channel1) # Внесение новых каналов в базу данных
        obnovlenie()

        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        await state.finish()

    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. Необходимо снова зайти в админ панель и выбрать нужный пункт')
        await state.finish()


# РЕДАКТИРУЕМ ВТОРОЙ КАНАЛ
@dp.callback_query_handler(text='change_trafik2') # Изменение каналов, на которые нужно подписаться
async def baza12342_2(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Отправь ссылку на новый, второй по счету канал\n',parse_mode='html',reply_markup=markup)
    await reg_trafik2.traf1.set()


@dp.message_handler(state=reg_trafik2.traf1, content_types='text')
async def traf_obnovlenie2(message: types.Message, state: FSMContext):
    await state.update_data(link_one = message.text)
    await bot.send_message(chat_id=message.chat.id, text=f'Теперь перешли мне любой пост из этого канала ({message.text})')
    await reg_trafik2.traf2.set()


@dp.message_handler(state=reg_trafik2.traf2, content_types=['text','photo','video'])
async def traf_obnovlenie_2(message: types.Message, state: FSMContext):
    link = await state.get_data()

    link_one = link['link_one'] #Ссылка на канал
    id_channel2 = (message.forward_from_chat.id) #ID канала

    try:
        obnovatrafika2(link_one, id_channel2) # Внесение 2-го новых каналов в базу данных
        obnovlenie()

        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        await state.finish()

    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. Необходимо снова зайти в админ панель и выбрать нужный пункт')
        await state.finish()


# РЕДАКТИРУЕМ ТРЕТИЙ КАНАЛ
@dp.callback_query_handler(text='change_trafik3') # Изменение каналов, на которые нужно подписаться
async def baza12342_3(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Отправь ссылку на новый, третий по счету канал\n',parse_mode='html',reply_markup=markup)
    await reg_trafik3.traf1.set()

@dp.message_handler(state=reg_trafik3.traf1, content_types='text')
async def traf_obnovlenie3(message: types.Message, state: FSMContext):
    await state.update_data(link_one = message.text)
    await bot.send_message(chat_id=message.chat.id, text=f'Теперь перешли мне любой пост из этого канала ({message.text})')
    await reg_trafik3.traf2.set()


@dp.message_handler(state=reg_trafik3.traf2, content_types=['text','photo','video'])
async def traf_obnovlenie_3(message: types.Message, state: FSMContext):
    link = await state.get_data()

    link_one = link['link_one'] #Ссылка на канал
    id_channel3 = (message.forward_from_chat.id) #ID канала

    try:
        obnovatrafika3(link_one, id_channel3) # Внесение 3-го новых каналов в базу данных
        obnovlenie()

        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        await state.finish()

    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. Необходимо снова зайти в админ панель и выбрать нужный пункт')
        await state.finish()

# РЕДАКТИРУЕМ ЧЕТВЕРТЫЙ КАНАЛ
@dp.callback_query_handler(text='change_trafik4') # Изменение каналов, на которые нужно подписаться
async def baza12342_4(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Отправь ссылку на новый, четвертый по счету канал\n',parse_mode='html',reply_markup=markup)
    await reg_trafik4.traf1.set()


@dp.message_handler(state=reg_trafik4.traf1, content_types='text')
async def traf_obnovlenie44(message: types.Message, state: FSMContext):
    await state.update_data(link_one = message.text)
    await bot.send_message(chat_id=message.chat.id, text=f'Теперь перешли мне любой пост из этого канала ({message.text})')
    await reg_trafik4.traf2.set()


@dp.message_handler(state=reg_trafik4.traf2, content_types=['text','photo','video'])
async def traf_obnovlenie_4(message: types.Message, state: FSMContext):
    link = await state.get_data()

    link_one = link['link_one'] #Ссылка на канал
    id_channel4 = (message.forward_from_chat.id) #ID канала

    try:
        obnovatrafika4(link_one, id_channel4) # Внесение 2-го новых каналов в базу данных
        obnovlenie()

        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        await state.finish()

    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. Необходимо снова зайти в админ панель и выбрать нужный пункт')
        await state.finish()

# РЕДАКТИРУЕМ Пятый КАНАЛ
@dp.callback_query_handler(text='change_trafik5') # Изменение каналов, на которые нужно подписаться
async def baza12342_5(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Отправь ссылку на новый, пятый по счету канал\n',parse_mode='html',reply_markup=markup)
    await reg_trafik5.traf1.set()


@dp.message_handler(state=reg_trafik5.traf1, content_types='text')
async def traf_obnovlenie55(message: types.Message, state: FSMContext):
    await state.update_data(link_one = message.text)
    await bot.send_message(chat_id=message.chat.id, text=f'Теперь перешли мне любой пост из этого канала ({message.text})')
    await reg_trafik5.traf2.set()


@dp.message_handler(state=reg_trafik5.traf2, content_types=['text','photo','video'])
async def traf_obnovlenie_5(message: types.Message, state: FSMContext):
    link = await state.get_data()

    link_one = link['link_one'] #Ссылка на канал
    id_channel5 = (message.forward_from_chat.id) #ID канала

    try:
        obnovatrafika5(link_one, id_channel5) # Внесение 5-го новых каналов в базу данных
        obnovlenie()

        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass
        await state.finish()

    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. Необходимо снова зайти в админ панель и выбрать нужный пункт')
        await state.finish()
#Конец обновлялки каналов


@dp.callback_query_handler(text='baza')
async def baza(call: types.callback_query):
    a = open('server.db','rb')
    await bot.send_document(chat_id=call.message.chat.id, document=a)




@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def check(call: types.callback_query):
    a = info_members() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Количество пользователей: {a}')


########################  Рассылка  ################################

@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.step_q.set()


@dp.callback_query_handler(text='otemena',state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    try:
        await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    except:
        pass

    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()



@dp.message_handler(state=st_reg.step_q,content_types=['text','photo','video','video_note']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id,text='Пост сейчас выглядит так 👆',reply_markup=murkap)



# НАСТРОЙКА КНОПОК
@dp.callback_query_handler(text='add_but',state=st_reg.st_name) # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправь мне кнопку по принципу\n\n'
                                                     'ИМЯ КНОПКИ - ССЫЛКА')
    await st_reg.step_regbutton.set()


@dp.message_handler(state=st_reg.step_regbutton,content_types=['text']) # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr2 = message.text.split('-')

    k = -1  # Убираем пробелы из кнопок
    for i in arr2:
        k+=1
        if i[0] == ' ':
            if i[-1] == ' ':
                arr2[k] = (i[1:-1])
            else:
                arr2[k] = (i[1:])

        else:
            if i[-1] == ' ':

                arr2[0] = (i[:-1])
            else:
                pass

    # arr2 - Массив с данными


    try:
        murkap = types.InlineKeyboardMarkup() #Клавиатура с кнопками
        bat = types.InlineKeyboardButton(text= arr2[0], url=arr2[1])
        murkap.add(bat)

        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,message_id=mess.message_id,reply_markup=murkap)

        await state.update_data(text_but =arr2[0]) # Обновление Сета
        await state.update_data(url_but=arr2[1])  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup() # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id,text='Теперь твой пост выглядит так☝',reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()


# КОНЕЦ НАСТРОЙКИ КНОПОК


@dp.callback_query_handler(text='send_ras',state="*") # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

    data = await state.get_data()
    mess = data['q'] # Сообщения для рассылки

    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    try: #Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_but = data['text_but']
        url_but = data['url_but']
        bat = types.InlineKeyboardButton(text=text_but, url=url_but)
        murkap.add(bat)
    except: pass


    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time").fetchall()
    bad = 0
    good = 0
    await bot.send_message(call.message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(1)
        try:
            await mess.copy_to(i[0],reply_markup=murkap)
            good += 1
        except:
            bad += 1

    await bot.send_message(
        call.message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
#########################################################