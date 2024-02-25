import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

import config
import database

# <<< Constants >>>
# Enter here your telegram id. @getmyid_bot may help you
admins = {1718021890}
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
    keyboard.add(InlineKeyboardButton(text='Items', callback_data='items'))
    keyboard.add(InlineKeyboardButton(text='My orders', callback_data='my_orders'))
    keyboard.add(InlineKeyboardButton(text='Developer', callback_data='developer'))

    await message.answer(f'Hi!, {message.from_user.mention}!', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'items')
async def process_callback_items(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await items(callback_query.message)


@dp.callback_query_handler(lambda c: c.data == 'my_orders')
async def process_callback_my_orders(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await my_orders(callback_query.message)


@dp.callback_query_handler(lambda c: c.data == 'developer')
async def process_callback_developer(callback_query: types.CallbackQuery):
    await callback_query.answer('Bot developer is @anekobtw\nTelegram channel: @anekobtww\nGithub: https://github.com/anekobtw')


# <<< Items >>>
@dp.message_handler(commands=['items'])
async def items(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    for key, value in config.items.items():
        keyboard.add(InlineKeyboardButton(text=f'{key} - {value}{config.currency}', callback_data=order_cb.new(action='create', item=key)))

    await message.answer(text='Choose the product to buy:', reply_markup=keyboard)


@dp.callback_query_handler(order_cb.filter(action='create'))
async def vote_up_cb_handler(query: types.CallbackQuery, callback_data: dict):
    item = callback_data['item']
    order_manager.insert_order(tgid=query.from_user.id, tg_nickname=query.from_user.full_name, product=item)
    latest_order = order_manager.get_active_orders()[-1]
    order_id = database.Order(*latest_order).order_id

    await bot.send_message(chat_id=query.from_user.id, text=f'You bought {item} that costs {config.items[item]}{config.currency}!\nOrder_id: {order_id}\n\nHowever, if it was an accident, you may delete your purchase by simply typing /delete_order {order_id}')
    await notify_admins_order(order_id=order_id)


# <<< My Orders >>>
@dp.message_handler(commands=['my_orders'])
async def my_orders(message: types.Message):
    await message.answer('under development')  # TODO: print user's orders


# <<< Admin commands >>>
@dp.message_handler(commands=['orders'])
async def orders(message: types.Message):
    arguments = message.get_args()
    if message.from_user.id in admins:
        orders = database.get_all_orders_by_status(arguments[0])
        for order in orders:
            await message.answer(database.get_order_info(order))


@dp.message_handler(commands=['next'])
async def next1(message: types.Message):
    await message.answer(database.get_first_order())


# <<< User-specific commands >>>
@dp.message_handler(commands=['delete_order'])
async def delete_order(message: types.Message):
    try:
        args = message.get_args()
        order_id = int(args.split()[0])
    except (ValueError, IndexError):
        await message.answer('The command is used incorrectly. Please, provide me with the order id. Example:\n/delete_order 4 ')
    else:
        order_manager.delete_order(order_id=order_id)
        await message.answer(f'Order {order_id} was deleted successfully.')

if __name__ == '__main__':
    executor.start_polling(dp)
