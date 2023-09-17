from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils import executor, exceptions
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from aiogram import types
import json

import database_review
import variables
import database

# Constants
admins = {1718021890, 1338590379}
web_app_info = WebAppInfo(url='') # insert here your website. it must be telegram web app. index.html is an example. 

# Initialize bot, storage, and dispatcher
storage = MemoryStorage()
bot = Bot(token=variables.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Helper Functions
async def change_status(message: types.Message, order_id: int, new_status: int) -> None:
    order_tgid = database.get_tgid(order_id)
    user_tgid = message.from_user.id
    if order_tgid == user_tgid or user_tgid in admins:
        database.set_order_status(order_id, new_status)
        await bot.send_message(chat_id=order_tgid, text=f'❗ Статус заказа был изменен\nАйди заказа: {order_id}\nНовый статус: {variables.status_states[new_status]}')

async def notify_admins_order(order_id: int) -> None:
    for admin_id in admins:
        await bot.send_message(chat_id=admin_id, text=f'❗ Поступил новый заказ!\nАйди заказа: {order_id}\n')


# inline buttons
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Заказать товар', callback_data='order'))
    keyboard.add(InlineKeyboardButton(text='Ссылки на соцсети', callback_data='links'))
    keyboard.add(InlineKeyboardButton(text='Отзывы', callback_data='reviews'))
    keyboard.add(InlineKeyboardButton(text='Разработчик', callback_data='developer'))
    
    await message.answer(f'Приветствую Вас, {message.from_user.mention}!\n\n{variables.start_message_template}', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'order')
async def process_callback_order(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await order(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'links')
async def process_callback_order(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await links(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'reviews')
async def process_callback_order(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await reviews(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'developer')
async def process_callback_order(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await developer(callback_query.message)

# Other commands
@dp.message_handler(commands=['links'])
async def links(message: types.Message):
    await message.answer(variables.links_template)

@dp.message_handler(commands=['developer'])
async def developer(message: types.Message):
    await message.answer('Разработчиком бота является @anekobtw\nТелеграм канал: @anekobtww\nГитхаб: https://github.com/anekobtw')

# secret commands (shhh)
@dp.message_handler(commands=['orders'])
async def orders(message: types.Message):
    arguments = message.get_args()
    if message.from_user.id in admins:
        try:
            orders = database.get_all_orders_by_status(arguments[0])
            for order in orders:
                await message.answer(database.get_order_info(order))
        except IndexError:
            await message.answer('/orders {status}\n\nСтатусы:\n0 - Ожидание принятия\n1 - Ожидание выполнения\n2 - Отклонено\n3 - Отменено\n4 - Выполнено')

@dp.message_handler(commands=['change_status'])
async def change_statuss(message: types.Message):
    arguments = message.get_args().split()
    if message.from_user.id in admins:
        await change_status(message, int(arguments[0]), int(arguments[1]))
        await message.answer('Готово!')

@dp.message_handler(commands=['next'])
async def next(message: types.Message):
    await message.answer(database.get_first_order())

    
# orders
@dp.message_handler(commands=['order'])
async def order(message: types.Message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Выберите товар")
    markup.add(types.InlineKeyboardButton('Открыть форму', web_app=web_app_info))
    
    await message.answer('Заполни форму.', reply_markup=markup)

@dp.message_handler(content_types=['web_app_data'])
async def web_app(message: types.Message):
    res = json.loads(message.web_app_data.data)

    premium = res["is_premium"].lower() == "да"
    database.insert(message.from_user.id, res["yt_nickname"], message.from_user.mention, res["order_type"], res["TA"], premium)
    await notify_admins_order()

    await message.answer("✅ Заказ успешно сделан! Напишите /my_orders, чтобы посмореть список Ваших заказов.")

@dp.message_handler(commands=["my_orders"])
async def my_orders(message: types.Message):
    orders = database.get_user_orders(message.from_user.id)
    if orders:
        for order in orders:
            await message.answer(database.get_order_info(order))
    else:
        await message.answer("У Вас нет заказов.")

@dp.message_handler(commands=['cancel_order'])
async def cancel_order(message: types.Message):
    try:
        order_id = message.get_args().split()[0]
    except IndexError:
        await message.answer('Команда использована неверно. Укажи айди заказа. Например:\n/cancel_order 4 ')
    else:
        try:
            await change_status(message, order_id, 3)
        except TypeError:
            await message.answer('Такого заказа не существует.')

# /review
@dp.message_handler(commands=['review'])
async def review(message: types.Message):
    arguments = message.get_args()
    try:
        a = arguments[0]
        database_review.insert(message.from_user.full_name, arguments)
        await message.answer('Благодарим за отзыв!')
    except IndexError:
        await message.answer('Команда использована неверно. Напиши отзыв. Например:\n/review Хорошее качество заказов, рекомендую')

@dp.message_handler(commands=['reviews'])
async def reviews(message: types.Message):
    try:
        await message.answer(database_review.get_all_reviews())
    except exceptions.MessageTextIsEmpty:
        await message.answer('Отзывов нет.')

if __name__ == '__main__':
    executor.start_polling(dp)
