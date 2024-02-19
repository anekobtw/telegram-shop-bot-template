from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

import config
import database

# <<< Constants >>>
# Enter here your telegram id. @getmyid_bot may help you
admins = {1718021890}


# <<< Initializing >>>
storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

async def notify_admins_order(order_id: int) -> None:
    for admin_id in admins:
        await bot.send_message(chat_id=admin_id, text=f'❗ Check out a new order!\nOrder id: {order_id}\n')


# <<< Inline buttons >>>
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Order', callback_data='order'))
    keyboard.add(InlineKeyboardButton(text='My orders', callback_data='my_orders'))
    keyboard.add(InlineKeyboardButton(text='Developer', callback_data='developer'))

    await message.answer(f'Hi!, {message.from_user.mention}!', reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'order')
async def process_callback_order(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await order(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'my_orders')
async def process_callback_order(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await my_orders(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'developer')
async def process_callback_order(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await developer(callback_query.message)


# <<< Commands >>>
@dp.message_handler(commands=['order'])
async def order(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    for i in config.items.keys:
        keyboard.add(InlineKeyboardButton(text=i, callback_data=config.items.values))

    await message.answer(reply_markup=keyboard)

@dp.message_handler(commands=['my_orders'])
async def my_orders(message: types.Message):
    await message.answer('')  # TODO: print user's orders

@dp.message_handler(commands=['developer'])
async def developer(message: types.Message):
    await message.answer('Bot developer is @anekobtw\nTelegram channel: @anekobtww\nGithub: https://github.com/anekobtw')


# <<< Admin commands >>>
@dp.message_handler(commands=['orders'])
async def orders(message: types.Message):
    arguments = message.get_args()
    if message.from_user.id in admins:
        orders = database.get_all_orders_by_status(arguments[0])
        for order in orders:
            await message.answer(database.get_order_info(order))

@dp.message_handler(commands=['next'])
async def next(message: types.Message):
    await message.answer(database.get_first_order())


# <<< User-specific commands >>>
@dp.message_handler(commands=['cancel_order'])
async def cancel_order(message: types.Message):
    try:
        order_id = int(message.get_args().split()[0])
    except (ValueError, IndexError):
        await message.answer('The command is used incorrectly. Please, insert the order id. Example:\n/cancel_order 4 ')
    else:
        database.delete(order_id)
        await message.answer(f'Order with id {order_id} was deleted successfully.')

if __name__ == '__main__':
    executor.start_polling(dp)
