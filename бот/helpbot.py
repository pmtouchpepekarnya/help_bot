import logging
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext


# Загрузка конфигурации
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
API_TOKEN = config['API_TOKEN']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class TimeOfDayStates(StatesGroup):
    choosing_time = State()

def start_command_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Утро", callback_data="morning"))
    keyboard.add(InlineKeyboardButton("День", callback_data="day"))
    keyboard.add(InlineKeyboardButton("Вечер", callback_data="evening"))
    return keyboard

@dp.message_handler(commands=['start'], state="*")
async def start_command(message: types.Message):
    await message.answer("Привет, я твой цифровой помощник, с чем у вас возникла проблема?", reply_markup=start_command_keyboard())
    await TimeOfDayStates.choosing_time.set()

def morning_questions_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Как начать смену?", callback_data="start_shift"))
    keyboard.add(InlineKeyboardButton("Как сделать утренний фотоотчет?", callback_data="morning_report"))
    keyboard.add(InlineKeyboardButton("Как сделать выкладку витрины?", callback_data="display_case"))
    keyboard.add(InlineKeyboardButton("Как заполнить стоп-лист?", callback_data="stop_list"))
    keyboard.add(InlineKeyboardButton("Назад", callback_data="back"))
    return keyboard


@dp.callback_query_handler(lambda c: c.data == 'morning', state=TimeOfDayStates.choosing_time)
async def handle_morning_button(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Вы выбрали 'Утро'. Что вас интересует?", reply_markup=morning_questions_keyboard())
    await state.finish()  # Сбрасываем состояние после выбора
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'start_shift')
async def handle_start_shift(callback_query: types.CallbackQuery):
    response_text = ("Чтобы начать смену, первым делом включите кофемашину и чайник.\n\n"
                     "Если вы не уверены, как это сделать, всегда можете спросить у бариста.\n\n"
                     "Не забудьте сделать утренний фотоотчет.\n\n"
                     "<b>Важно: все фотоотчеты должны быть сделаны до 8:00!</b>")
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton("Назад", callback_data="back"))
    await bot.send_message(callback_query.from_user.id, response_text, reply_markup=back_button, parse_mode='HTML')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'morning_report')
async def handle_morning_report(callback_query: types.CallbackQuery):
    # Отправляем первую часть текста
    await bot.send_message(callback_query.from_user.id, "<b>Фотография открытой смены пример: </b>", parse_mode='HTML')
    
    # Отправляем первую фотографию
    await bot.send_photo(callback_query.from_user.id, photo=open('picture/morning/image-000.jpg', 'rb'))

    # Отправляем вторую часть текста
    await bot.send_message(callback_query.from_user.id, "<b>Внешний вид смены пример: </b>", parse_mode='HTML')

    # Отправляем вторую фотографию
    await bot.send_photo(callback_query.from_user.id, photo=open('picture/morning/image-001.jpg', 'rb'))

    # Отправляем третью часть текста
    await bot.send_message(
    callback_query.from_user.id,
    "<b>ВНИМАНИЕ!</b> \n"
    "Ваш внешний вид должен соответствовать стандартам: \n"
    "1. Однотонный низ и черный верх. \n "
    "2. Фартук и кепка соответственно (для девочек косынка).",  
    parse_mode='HTML')

    # Клавиатура с кнопкой "Назад"
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton("Назад", callback_data="back"))
    await bot.send_message(callback_query.from_user.id, "Выберите дальнейшее действие:", reply_markup=back_button)

    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'display_case')
async def handle_display_case(callback_query: types.CallbackQuery):
    # Отправляем фотографию витрины
    await bot.send_photo(callback_query.from_user.id, photo=open('picture/morning/vitrina.jpg', 'rb'))

    # Отправляем текст о выкладке
    text_vitrina = (
        "Витрина с выпечкой должна выглядеть так как на фото, не нужно наваливать друг на друга выпечку, "
        "она продавливается под весом, если у вас слишком много выпечки и она не помещается, "
        "можно отложить немного в контейнер. Всё выглядит аккуратно и красиво, так и должно быть."
    )
    await bot.send_message(callback_query.from_user.id, text_vitrina)

    # Отправляем вторую фотографию с расположением продукции
    await bot.send_photo(callback_query.from_user.id, photo=open('picture/morning/raspolozhenie.jpg', 'rb'))

    # Отправляем текст о расположении продукции
    text_raspolozhenie = (
        "Расположение холодильной витрины\n"
        "Первая полочка: Макарунсы, Эклеры, немного пирожных, пончики\n"
        "Вторая полка: пирожные\n"
        "Третья полка: чизкейки\n\n"
        "<b><i>Важно!!! Чтобы десерты не выходили за подложки, а круассаны за крафт бумагу!!</i></b>"
    )
    await bot.send_message(callback_query.from_user.id, text_raspolozhenie, parse_mode='HTML')

    # Клавиатура с кнопкой "Назад"
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton("Назад", callback_data="back"))
    await bot.send_message(callback_query.from_user.id, "Выберите дальнейшее действие:", reply_markup=back_button)

    await bot.answer_callback_query(callback_query.id)
@dp.callback_query_handler(lambda c: c.data == 'stop_list')
async def handle_stop_list(callback_query: types.CallbackQuery):
    # Отправляем текстовое сообщение
    response_text = (
        "После того как все десерты и выпечка выложены, и вы выглядите нормально для "
        "работника общепита, а ваши мешки под глазами можно заправлять в штаны, пришло время вбивать стоп-лист. Выпечку и десерты нужно "
        "обязательно пересчитать, чтобы избежать расхождений в инвентаре."
    )
    await bot.send_message(callback_query.from_user.id, response_text)

    # Отправляем инструкцию с фото
    instruction_text = "Заходим в меню, это можно сделать нажав три полоски сверху, само меню выглядит так:"
    await bot.send_message(callback_query.from_user.id, instruction_text)
    
    # Отправляем фото меню
    await bot.send_photo(callback_query.from_user.id, photo=open('picture/morning/menu.jpg', 'rb'))
 
    # Дополнительные инструкции
    additional_text = (
        "Вам нужно нажать кнопку 'Стоп-лист'. Это меню стоп листа, в котором вы начинаете забивать "
        "количество позиций по списку, который вы пересчитали."
    )
    await bot.send_message(callback_query.from_user.id, additional_text)
    # Отправляем фото меню
    await bot.send_photo(callback_query.from_user.id, photo=open('picture/morning/stop_list.jpg', 'rb'))
    # Отправляем фото чека
    await bot.send_photo(callback_query.from_user.id, photo=open('picture/morning/edit_stop_list.jpg', 'rb'))
    # Отправляем инструкцию с фото
    check_text ="После того как забили всё по списку, и проверили "
    "нужно будет нажать на кнопку печать," 
    "она вон там в углу снизу./n" 
    "У вас вылезет большой чек, который нужно будет сфотографировать с листом прихода",
    await bot.send_message(callback_query.from_user.id, check_text)
    await bot.send_photo(callback_query.from_user.id, photo=open('picture/morning/check_photo.jpg', 'rb'))
# Клавиатура с кнопкой "Назад"
    back_button = InlineKeyboardMarkup()
    back_button.add(InlineKeyboardButton("Назад", callback_data="back"))
    await bot.send_message(callback_query.from_user.id, "Выберите дальнейшее действие:", reply_markup=back_button)

    await bot.answer_callback_query(callback_query.id)
    

# ... (аналогичные обработчики для других кнопок) ...

@dp.callback_query_handler(lambda c: c.data == 'back')
async def handle_back_button(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выберите один из вариантов:", reply_markup=start_command_keyboard())
    await TimeOfDayStates.choosing_time.set()  # Возвращаем пользователя в начальное состояние
    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
