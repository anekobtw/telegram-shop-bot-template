import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

import config
import database

# <<< Constants >>>
admins = config.admins
order_manager = database.OrderManager()
order_cb = CallbackData('order', 'action', 'item')


# <<< Initializing >>>
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO, filename='log.txt')


async def notify_admins_order(order_id: int) -> None:
    for admin_id in admins:
        await bot.send_message(chat_id=admin_id, text=f'❗ Check out a new order!\nOrder id: {order_id}\n')


# <<< Inline start buttons >>>
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Check the shop', callback_data='items'),
                 InlineKeyboardButton(text='My orders', callback_data='my_orders'),
                 InlineKeyboardButton(text='Developer', callback_data='developer'))

    await message.answer(f'Hi!, {message.from_user.mention}!', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'items')
async def process_callback_items(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await items(callback_query.message)


@dp.callback_query_handler(lambda c: c.data == 'my_orders')
async def process_callback_my_orders(callback_query: types.CallbackQuery):
    await callback_query.answer()
    orders_data = order_manager.get_user_orders(callback_query.from_user.id)
    if orders_data:
        orders_text = "\n".join(database.Order(*order_data).all_data() for order_data in orders_data)
        await bot.send_message(chat_id=callback_query.from_user.id, text=orders_text)
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text="You don't have any orders yet.")


@dp.callback_query_handler(lambda c: c.data == 'developer')
async def process_callback_developer(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.from_user.id, text='''Bot developer is @anekobtw
Telegram channel: @anekobtww
Github: https://github.com/anekobtw
Source code of this bot: https://github.com/anekobtw/telegram-shop-bot''')


# <<< Items >>>
@dp.message_handler(commands=['items'])
async def items(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    for item, price in config.items.items():
        keyboard.add(InlineKeyboardButton(text=f'{item} - {price}{config.currency}',
                                          callback_data=order_cb.new(action='create', item=item)))

    await message.answer(text='Choose the product to buy:', reply_markup=keyboard)


@dp.callback_query_handler(order_cb.filter(action='create'))
async def order_cb_handler(query: types.CallbackQuery, callback_data: dict):
    item = callback_data['item']
    order_manager.insert_order(query.from_user.id, query.from_user.full_name, item)
    order_id = database.Order(*order_manager.get_active_orders()[-1]).order_id

    text = f'''You\'ve bought {item} that costs {config.items[item]}{config.currency}
Order_id: {order_id}
However, if it was an accident, you may delete your purchase by simply typing /delete_order {order_id}'''
    await bot.send_message(chat_id=query.from_user.id, text=text)
    await notify_admins_order(order_id=order_id)


# <<< Admin commands >>>
@dp.message_handler(commands=['orders'])
async def orders(message: types.Message):
    if message.from_user.id in admins:
        orders_data = order_manager.get_active_orders()
        for order_data in orders_data:
            order_obj = database.Order(*order_data)
            await message.answer(order_obj.all_data())


@dp.message_handler(commands=['next'])
async def next1(message: types.Message):
    orders_data = order_manager.get_active_orders()
    order_obj = database.Order(*orders_data[0])
    await message.answer(order_obj.all_data())


# <<< Others >>>
@dp.message_handler(commands=['delete_order'])
async def delete_order(message: types.Message):
    try:
        args = message.get_args()
        order_id = int(args.split()[0])
    except (ValueError, IndexError):
        await message.answer('The command is used incorrectly. Please, provide me with the order id. Example:\n/delete_order 4 ')
    else:
        order_data = order_manager.get_order(order_id)
        if database.Order(*order_data).tgid == message.from_user.id:
            order_manager.delete_order(order_id=order_id)
            await message.answer(f'Order {order_id} was deleted successfully.')

if __name__ == '__main__':
    executor.start_polling(dp)
