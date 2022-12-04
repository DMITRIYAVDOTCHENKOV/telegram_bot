from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo



bot = Bot(token="5954278124:AAGu9G58KGe8K4PNP1FPGmkTASXmypjA6YY")
db = Dispatcher(bot)


@db.message_handler(commands=['start'])
async def begin(message: types.message):
    await bot.send_message(message.chat.id, "Привет!")


# отоброжаем кнопки в боте
@db.message_handler(commands=['button'])
async def button(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('ютуб', callback_data='b1')
    item2 = types.InlineKeyboardButton('wiki', callback_data='b4')
    markup.add(item, item2)
    await bot.send_message(message.chat.id, 'Привет!', reply_markup=markup)


# обработка кнопок, не могу к ним подключить функции, везде только сообщения или ссылки, но блин что бы нажал, и заработала
# другая кнопка, не моуг найти...два дня лазил.... если знаете как можете показать, или ссылку скинуть почитаю
@db.callback_query_handler(lambda call: True)
async def callback_inline(call):
    if call.message:
        if call.data == 'b1':
            await bot.send_message(call.message.chat.id,
                                   'Я пока не знаю как сюда подключить перех на ютуп, поэтому введи'
                                   'команду /b4 и ты сможешь посмотреть ютуб, либо просто'
                                   'перейди по ссылки' + '[ссылке](https://www.youtube.com/')
        elif call.data == 'b4':
            await bot.send_message(call.message.chat.id,
                                   'Я еще не научился искать что то в википедии, но если очень хочешь'
                                   'можешь просто ввести , что то, и я найду в вкипедии тебе материал.'
                                   'Либо ищи сам по ссылки =))' + '[ссылке](https://ru.wikipedia.org')


# тоже пытался обработку кнопки сделать для ссылки
@db.message_handler(commands=['b1'])
async def button_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="wikipedia", callback_data="button_1")
    markup.add(button)

    await bot.send_message(message.chat.id, 'Text', reply_markup=markup)


@db.callback_query_handler(lambda c: c.data == "button_1")
async def button_3(call: types.callback_query):
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, 'Нажата')


# переход на ютуб, нашел интересный метот, получается маленькое окошко отркывается прям поверх телеграмма, удобно )
@db.message_handler(commands=['b4'])
async def button_4(message: types.Message):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Ютуб", web_app=WebAppInfo(url="https://www.youtube.com/"))
    markup.add(button)

    await bot.send_message(message.chat.id, 'Text', reply_markup=markup)


# это получается парсинг с википедией, но я не смогу разобраться как сделать по кнопки, или типа зделать запрос.
# в итоге ищет что то просто по тексту в чат, и кидает фото и ссылку.
@db.message_handler(content_types=['text'])
async def begin(message: types.message):
    url = "https://ru.wikipedia.org/w/index.php?go=Перейти&search=" + message.text
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")

    links = soup.find_all("div", class_="mw-serch-result-heading")

    if len(links) > 0:
        url = "https://ru.wikipedia.org" + links[0].find("a")["href"]

    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=option)
    driver.get(url)

    driver.execute_script("window.scrollTo(0,200)")
    driver.save_screenshot("img.png")
    driver.close()

    photo = open("img.png", 'rb')
    await bot.send_photo(message.chat.id, photo=photo, caption=f'Ссылка на статью: <a href="{url}">тык</a>',
                         parse_mode="HTML")


executor.start_polling(db)
