from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from ruSpamLib import is_spam
import json

# Инициализация бота с токеном
bot = Bot(token="7311526472:AAH7Jj5rN1iivkigRjNrXvvmcvabsqRoDvY")

# Инициализация диспетчера
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    inline_kb = InlineKeyboardMarkup(row_width=2)
    inline_kb.add(
        InlineKeyboardButton("Админ панель👀", callback_data='button'),
    )

    start_message = await message.answer(f'<b>Привет, {message.from_user.first_name}</b>\n\nЯ бот для проверки спама. Просто пригласи меня в группу и я буду удалять все спам сообщения.\n\nТак же у меня есть админ панель, просто нажми на кнопку ниже и тебе откроются расширенные настройки.\n\nУдачного использования!\n\n<i>Админы: @FlorikX, @NeuroSpaceX</i>', parse_mode='html', reply_markup=inline_kb)
    dp['start_message_id'] = start_message.message_id


@dp.callback_query_handler(lambda c: c.data)
async def process_callback_button(callback_query: types.CallbackQuery):
    start_message_id = dp.get('start_message_id')
    data = callback_query.data
    if data == 'button':
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=start_message_id)
        await bot.send_message(callback_query.from_user.id, "<b>Админ панель👀</b>\n\nСейчас админ панель только в разработке...", parse_mode='html')


@dp.message_handler(lambda message: True)  # Обрабатываем все сообщения
async def spam(message: types.Message):
    pred_average = is_spam(message.text, model_name="spamNS_large_v1")
    
    if pred_average:  # Если сообщение определено как спам
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)  # Удаляем сообщение
        await bot.send_message(message.chat.id, "Сообщение удалено, так как оно было определено как спам.")
    
# Запуск long-polling
if __name__ == '__main__':
    executor.start_polling(dp)
