import asyncio
import logging
import tokenStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=tokenStorage.TOKEN)
# Диспетчер
dp = Dispatcher()

value = ''
old_value = ''

builder = InlineKeyboardBuilder()
builder.row(types.InlineKeyboardButton(text=' ', callback_data='no'),
                types.InlineKeyboardButton(text='C', callback_data='C'),
                types.InlineKeyboardButton(text='<=', callback_data='<='),
                types.InlineKeyboardButton(text='/', callback_data='/'))
builder.row(types.InlineKeyboardButton(text='7', callback_data='7'),
                types.InlineKeyboardButton(text='8', callback_data='8'),
                types.InlineKeyboardButton(text='9', callback_data='9'),
                types.InlineKeyboardButton(text='*', callback_data='*'))
builder.row(types.InlineKeyboardButton(text='4', callback_data='4'),
                types.InlineKeyboardButton(text='5', callback_data='5'),
                types.InlineKeyboardButton(text='6', callback_data='6'),
                types.InlineKeyboardButton(text='-', callback_data='-'))
builder.row(types.InlineKeyboardButton(text='1', callback_data='1'),
                types.InlineKeyboardButton(text='2', callback_data='2'),
                types.InlineKeyboardButton(text='3', callback_data='3'),
                types.InlineKeyboardButton(text='+', callback_data='+'))
builder.row(types.InlineKeyboardButton(text=' ', callback_data='no'),
                types.InlineKeyboardButton(text='0', callback_data='0'),
                types.InlineKeyboardButton(text='.', callback_data='.'),
                types.InlineKeyboardButton(text='=', callback_data='='))

@dp.message(Command("start"))
async def cmd_start(message):
    global value
    if value == '':
        await bot.send_message(message.from_user.id, '0', reply_markup=builder.as_markup())
    else:
        await bot.send_message(message.from_user.id, value, reply_markup=builder.as_markup())

        # await bot.send_message(message.from_user.id, '0', reply_markup=builder.as_markup())

# @dp.message(F.text == 'Start calculating')
# async def calculating(message: types.Message):

    # await message.answer('Нажмите на кнопку:', reply_markup=builder.as_markup())



@dp.callback_query()
async def callbacks(callback: types.CallbackQuery):
    data = callback.data
    global value, old_value

    if data == 'no':
        pass
    elif data == 'C':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value) - 1]
    elif data == '=':
        try:
            value = str(eval(value))
        except:
            value = 'Ошибка'
    else:
        value += data

    if (value != old_value and value != '') or (old_value != '0' and value != ''):
        if value == '':
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='0', reply_markup=builder.as_markup())
            old_value = '0'
        else:
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=value, reply_markup=builder.as_markup())
            old_value = value

    if value == 'Ошибка':
        value = ''









# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
