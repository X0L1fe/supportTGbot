import asyncio
import logging


from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram import F
from aiogram import html


from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.utils.formatting import Text, Bold
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ContentType
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram.filters import Command
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest



#Импорт из файла инлайн кейбоард





Bot_token = '7004277965:AAEVMQ4YmuLG1CAZqQ5ntNWlbY9RSqZr06o'

bot = Bot(token='7004277965:AAEVMQ4YmuLG1CAZqQ5ntNWlbY9RSqZr06o')
dp = Dispatcher()

async def main():

  logging.basicConfig(filename="log.txt",
                      filemode='w',
                      level=logging.INFO)
  await dp.start_polling(bot)

#----------------------------------------------




@dp.message(F.text.lower() == "меню:")
async def with_puree(message: types.Message):
    builder = ReplyKeyboardBuilder()

    builder.row(
            types.KeyboardButton(text="Наши магазины и номера для связи:"),
            types.KeyboardButton(text="Наш сайт:")
    ),
    builder.row(
            types.KeyboardButton(text="Номер для связи с администратором сети магазинов")
    )
    builder.row(
            types.KeyboardButton(text="Ассортимент"),
            types.KeyboardButton(text="Поддержка"),
    )
    await message.answer(f'Выберите категорию:', reply_markup=builder.as_markup(resize_keyboard=True))




#Начало работы с сайтом.
@dp.message(Command('start'))
async def cmd_start(message: Message):
    content = Text (
        'Здравствуйте!', ' ',(message.from_user.full_name),'.',' ',
        'Добро пожаловать в телеграмм магазин: Старик Хоттабыч!'

    )
    await message.answer(
        **content.as_kwargs()
    )
    builder = ReplyKeyboardBuilder()

    builder.row(
            types.KeyboardButton(text="Наши магазины и номера для связи:"),
            types.KeyboardButton(text="Наш сайт:")
    ),
    builder.row(
            types.KeyboardButton(text="Номер для связи с администратором сети магазинов")
    )
    builder.row(
            types.KeyboardButton(text="Ассортимент"),
            types.KeyboardButton(text="Поддержка"),
    )
    await message.answer("Есть огромное желание покурить кальян но нет никакого желания ехать за всем необходимым самому? "
                         "У нас есть выход для тебя! 1. Ты можешь приобрести у нас все, что тебе нужно на сайте, и тебе доставят"
                         " это прямиком до двери! 2. Мы самолично привезем тебе кальян в полной комплектации и на следующий день самолично заберем ;)"
                         "3. Хочешь покурить дома или намечается крутая вечеринка, но делать кальян самому нет никакого желания или возможности? "
                         "Можешь воспользоваться нашей услугой: Выезд кальянщика. Он приедет и сделает тебе крутой кальян ;)", reply_markup=builder.as_markup(resize_keyboard=True))




#Меню

#......................

#Наш сайт
@dp.message(F.text.lower() == "наш сайт:")
async def with_puree(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Перейти на сайт",url='https://starikpnz.ru')
    )
    await message.answer("Ссылка на наш сайт: https://starikpnz.ru", reply_markup=builder.as_markup())


#Админ связь

@dp.message(F.text.lower() == "номер для связи с администратором сети магазинов")
async def svyaz_admin(message: types.Message):

  builder = InlineKeyboardBuilder()
  builder.add(types.InlineKeyboardButton(text="Номер для связи с администратором сети магазинов", callback_data='admin_number'))


  await message.answer(
    'Выберите магазин чтобы увидеть номер телефона для связи с ним',
    reply_markup=builder.as_markup(resize_keyboard=True)
          )

@dp.callback_query(F.data == 'admin_number')
async def adm(callback: types.CallbackQuery):
    await callback.answer(
        text="Номер для связи с администратором сети магазинов: +7 (962) 470-78-88",
        show_alert=True
    )

#.....................



#Адреса




def adresa():
    buttons = [
        [
            types.InlineKeyboardButton(text="ул. Московская, 8", callback_data='adresone'),
            types.InlineKeyboardButton(text="ул. Московская 70", callback_data='adrestwo')
        ],
        [types.InlineKeyboardButton(text="ул. Бородина 2", callback_data='adresthree')
         ],
        [
         types.InlineKeyboardButton(text="ТЦ Суворовский, ул.Суворова, 144а", callback_data='adresfour')
        ],
        [
            types.InlineKeyboardButton(text="Пармаркет, Измайлова 58а", callback_data='adresfive')
            ],
        [
            types.InlineKeyboardButton(text="Генерала Глазунова 3", callback_data='adressix')
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard



@dp.message(F.text.lower() == "наши магазины и номера для связи:")
async def cmd_numbers(message: types.Message):
    await message.answer("Выберите магазин чтобы увидеть номер телефона для связи с ним", reply_markup=adresa())






@dp.callback_query(F.data == 'adresone')
async def adres1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Номер телефона магазина по адресу:г. Пенза, ул. Московская, 8:+7 (962) 471-55-50')



@dp.callback_query(F.data == 'adrestwo')
async def adres2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Номер телефона магазина по адресу:Пенза, ул. Московская 70,+7 (927) 365-82-70")


@dp.callback_query(F.data == 'adresthree')
async def adres3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Номер телефона магазина по адресу:г. Пенза, ул. Бородина 2, +7 (963) 100-73-68")



@dp.callback_query(F.data == 'adresfour')
async def adres4(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Номер телефона магазина по адресу:ТЦ Суворовский г.Пенза, ул.Суворова, 144а,:*не указан*")


@dp.callback_query(F.data == 'adresfive')
async def adres6(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Номер телефона магазина по адресу:Пармаркет Пенза, Измайлова 58а (Пармаркет),:*+7 (927) 289-29-47*")


@dp.callback_query(F.data == 'adressix')
async def adres7(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,"Номер телефона магазина по адресу:Пенза, Генерала Глазунова 3,:*Не указан*"
    )




def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Под", callback_data='pod'),
            types.InlineKeyboardButton(text="Чаши", callback_data='chashi')
        ],
        [types.InlineKeyboardButton(text="Кальян", callback_data='kalik'),
         types.InlineKeyboardButton(text="Жидкость", callback_data='zid')
        ],
        [
            types.InlineKeyboardButton(text="Что-то еще", callback_data='chtoto')
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@dp.message(F.text.lower() == "ассортимент")
async def cmd_numbers(message: types.Message):
    await message.answer("Выберите категорию:", reply_markup=get_keyboard())



@dp.callback_query(F.data == 'chashi')
async def pod(callback: types.CallbackQuery):
    await callback.answer(
        text="Чаши для примера",
        show_alert=True
    )

@dp.callback_query(F.data == 'pod')
async def podiki(callback: types.CallbackQuery):
    await callback.answer(
        text="Подики для примера",
        show_alert=True
    )

@dp.callback_query(F.data == 'kalik')
async def podiki(callback: types.CallbackQuery):
    await callback.answer(
        text="калик",
        show_alert=True
    )

@dp.callback_query(F.data == 'zid')
async def podiki(callback: types.CallbackQuery):
    await callback.answer(
        text="Жидкость",
        show_alert=True
    )

@dp.callback_query(F.data == 'chtoto')
async def podiki(callback: types.CallbackQuery):
    await callback.answer(
        text="Что-то",
        show_alert=True
    )
@dp.message(F.text.lower() == "жидкость")
async def cmd_inline_url(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="жижа 1",callback_data='zidkost1')
    )
    builder.row(types.InlineKeyboardButton(
        text="жижа 2",callback_data='zidkost2')
    )
    builder.row(types.InlineKeyboardButton(
        text="жижа 3",callback_data='zidkost3')
    )
    await message.answer(
            'Выберите интересующую Вас крепость',
            reply_markup=builder.as_markup()
        )
# Поддержка
@dp.message(F.text.lower() == "поддержка")
async def with_puree(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Меню:")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажмите 'меню:' чтобы вернуться назад"
    )
    await message.answer("https://t.me/PhotoPainterSupport_bot",
                         reply_markup=keyboard)




# Ответ на пустые сообщения:
@dp.message()
async def start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Меню:")

        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажмите 'Меню:'"
    )
    await message.answer('Здравствуй! К сожалению, я не понимаю Вас. Введите "Меню:", чтобы вернуться к меню',
                         reply_markup=keyboard)


# Функция чтобы бот не отключался
if __name__ == "__main__":
    asyncio.run(main())