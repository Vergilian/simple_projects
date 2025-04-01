from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserInfo(StatesGroup):
    age = State()
    weight = State()
    height = State()
    gender = State()


menu = InlineKeyboardMarkup()
menu.add(InlineKeyboardButton('1. Расчитать калории', callback_data='calculate'),
         InlineKeyboardButton('2. Информация', callback_data='info'),
         InlineKeyboardButton('3. 🔙 Главное меню', callback_data='main_menu'))

gender_b = InlineKeyboardMarkup()
gender_b.add(InlineKeyboardButton('1. Мужской', callback_data='male'),
              InlineKeyboardButton('2. Женский', callback_data='female'),
              InlineKeyboardButton('3. 🔙 Главное меню', callback_data='main_menu'))

main_b = InlineKeyboardMarkup()
main_b.add(InlineKeyboardButton('🔙 3. Главное меню', callback_data='main_menu'))




# Модифицированные функции, которые обрабатывают текстовые сообщения
async def process_calculation_from_message(message: types.Message):
    await message.answer('Хорошо. Укажи свой возраст: ', reply_markup=main_b)
    await UserInfo.age.set()


async def process_info_from_message(message: types.Message):
    await message.answer('Этот бот поможет рассчитать твою суточную норму калорий по формуле Миффлина-Сан Жеора.')
    await message.answer("Выбери действие:", reply_markup=menu)


async def go_to_main_menu(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=menu)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет, выбери что ты хочешь: ', reply_markup=menu)


@dp.callback_query_handler(lambda c: c.data == "info")
async def process_info(call: types.CallbackQuery):
    await call.answer('Этот бот поможет рассчитать твою суточную норму калорий по формуле Миффлина-Сан Жеора.')
    await call.message.answer("Выбери действие:", reply_markup=menu)


@dp.callback_query_handler(lambda c: c.data == "calculate")
async def process_calculation(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer('Хорошо. Укажи свой возраст: ', reply_markup=main_b)
    await UserInfo.age.set()


@dp.callback_query_handler(lambda c: c.data == "main_menu", state='*')
async def process_main_menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await go_to_main_menu(call.message)
    await state.finish()


@dp.message_handler(state=UserInfo.age)
async def process_age(message: types.Message, state: FSMContext):
    if message.text.lower() in ["меню", "3"]:
        await go_to_main_menu(message)
        await state.finish()
        return

    if not message.text.isdigit():
        await message.answer('Введи корректный возраст(число)')
        return

    await state.update_data(age=int(message.text))
    await message.answer("Отлично! Теперь введи свой вес (в кг)", reply_markup=InlineKeyboardMarkup().add(
        InlineKeyboardButton('3. 🔙 Главное меню', callback_data='main_menu')))
    await UserInfo.weight.set()


@dp.message_handler(state=UserInfo.weight)
async def process_weight(message: types.Message, state: FSMContext):
    if message.text.lower() in ["меню", "3"]:
        await go_to_main_menu(message)
        await state.finish()
        return

    if not message.text.isdigit():
        await message.answer("Введите корректный вес (число).")
        return

    await state.update_data(weight=int(message.text))
    await message.answer("Теперь укажи свой рост (в см).", reply_markup=InlineKeyboardMarkup().add(
        InlineKeyboardButton('3. 🔙 Главное меню', callback_data='main_menu')))
    await UserInfo.height.set()


@dp.message_handler(state=UserInfo.height)
async def process_height(message: types.Message, state: FSMContext):
    if message.text.lower() in ["меню", "3"]:
        await go_to_main_menu(message)
        await state.finish()
        return

    if not message.text.isdigit():
        await message.answer("Введите корректный рост (число).")
        return

    await state.update_data(height=int(message.text))
    await message.answer("Выбери свой пол:", reply_markup=gender_b)
    await UserInfo.gender.set()


@dp.callback_query_handler(lambda c: c.data in ["male", "female"], state=UserInfo.gender)
async def process_gender(call: types.CallbackQuery, state: UserInfo.gender):
    gender = call.data.lower()
    if gender == 'male':
        gender_text = 'Мужской'
    else:
        gender_text = 'Женский'

    user_data = await state.get_data()
    age = user_data['age']
    weight = user_data['weight']
    height = user_data['height']

    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    await call.message.answer(f"Твой базовый уровень метаболизма (BMR): {bmr:.2f} ккал/день.\n"
                              f"Пол: {gender_text}\n"
                              "Это количество калорий, необходимое организму в состоянии покоя.",
                              reply_markup=menu)

    await state.finish()


@dp.message_handler(lambda message: message.text in ["1", "2", "1. Рассчитать калории", "2. Информация", "3", 'меню'])
async def handle_button(message: types.Message):
    if message.text == "1" or message.text == "1. Рассчитать калории":
        await process_calculation_from_message(message)
    elif message.text == "2" or message.text == "2. Информация":
        await process_info_from_message(message)
    elif message.text == "3" or message.text == "меню":
        await go_to_main_menu(message)


@dp.message_handler(commands=['private'])
async def send_private_button(message: types.Message):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Написать в личку", url=f"https://t.me/Drunk_teachers_bot")
    )
    await message.answer("Нажми на кнопку, чтобы бот написал тебе в личные сообщения:", reply_markup=keyboard)
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
