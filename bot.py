import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import BotCommand
from aiogram import F
from datetime import datetime
from config_reader import config 
from stickerslist import stickers
from random import choice

# Логирование
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")




# Меню
async def set_main_menu(bot:Bot):

    main_menu_commands = [
        BotCommand(command='/start',
                   description= 'Начало работы с ботом'),
        BotCommand(command='/sticker',
                   description='Прислать рандомный стикер')
    ]
    await bot.set_my_commands(main_menu_commands)


# Вывод времени работы бота
@dp.message(Command("info"))
async def cmd_info(message: types.Message, started_at: str):
    await message.answer(f"Бот запущен {started_at}")



# Хэндлер на команду /start 
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Пришли стикер")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    
    await message.reply("Привет! Я могу прислать тебе рандомный стикер обезьяны \n"
                        "Напиши <b><u>Пришли стикер</u></b> или нажми кнопку снизу", 
                        reply_markup=keyboard,
                        parse_mode = "html")




# Вывод стикера по кнопке
@dp.message(F.text.lower() == "пришли стикер")
async def send_stick(message: types.Message):
    await bot.send_sticker(chat_id = message.chat.id, sticker = choice(stickers))


# Хэндлер на сообщение Привет
@dp.message(F.text.lower() == "привет")
async def cmd_privet(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Пришли стикер")],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.reply("Привет, привет! Я могу отправить тебе стикер обезьянки просто напиши <пришли стикер> или нажми кнопку снизу")


# Вывод рандомного стикера из пула
@dp.message(Command("sticker"))
async def send_stick(message: types.Message):
    await bot.send_sticker(chat_id = message.chat.id, sticker = choice(stickers))

# Реакция на другие сообщения кроме описанных
@dp.message()
async def send_echo(message: types.Message):
    await message.answer(
        text = "Не понял\nЧтобы узнать, что делает этот бот, напиши команду /start\n"
                "Или просто напиши <b><u>Пришли стикер</u></b>",
                parse_mode="html"
    )
    

    
# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)
    



if __name__ == "__main__":
    dp.startup.register(set_main_menu)
    asyncio.run(main())

