from aiogram import types
from create_bot import bot, Dispatcher, dp
from bot_source.other.utilities import cenz
import asyncio
from aiogram.utils.exceptions import Throttled
from create_bot import storage
from bot_source.database import sqlite_db
from datetime import datetime, timedelta

last_message_time = {}

async def start(msg: types.Message):
    await bot.send_message(msg.from_user.id, f"Привет, {msg.from_user.username}!\nТы попал в онлайн чат бара 'Крафтов'. Здесь ты можешь отправить сообщение, которое посетители бара "
                                             f"увидят на экране. Передавай приветы, поздравления, рекомендации по выбору пива:). Наши гости с удовольствием тебе ответят.\nВведи /rules, чтобы узнать правила.")
    await sqlite_db.insert_new_user(msg)


async def anti_flood(m: types.Message):
    user_id = m.from_user.id

    if user_id in last_message_time:
        time_since_last_message = datetime.now() - last_message_time[user_id]
        if time_since_last_message < timedelta(seconds=60):
            time_left = int((timedelta(seconds=60) - time_since_last_message).total_seconds())
            await m.answer(f"Вы можете отправлять не более 1 сообщения в минуту\nПодождите еще {time_left} секунд(ы)")
            return False

    last_message_time[user_id] = datetime.now()
    return True


async def cmd_rules(msg: types.Message):
    await bot.send_message(msg.from_user.id, "Правила:\n"
                                       "1. Ты можешь отправить не более одного сообщения в минуту.\n"
                                       "2. У нас нельзя нецензурно выражаться и оскорблять других участников. За нарушение этого пункта вы получаете предупреждение, если наберете 5 предупреждений, то будете заблокированы.\n"
                                       "3. Твое сообщение отображается 30 секунд, но если кто-то написал быстрее тебя, то сообщение попадет в очередь и будет показано позже.\n"
                                       "4. Нельзя писать слишком длинные сообщения. Максимальная длинна 110 символов.")


async def get_message(msg: types.Message):
    if await anti_flood(msg):

        if len(msg.text) < 110:
            if sqlite_db.check_for_ban(msg) == True:
                if await cenz(msg):
                    await bot.send_message(msg.from_user.id, 'Предупреждение: у нас нельзя материться')
                    sqlite_db.increase_count(msg)
                else:
                    mod_msg = f'{msg.from_user.username} пишет: {msg.text}'
                    await sqlite_db.insert_comment(msg, mod_msg)
                    # await bot.send_message(chat_id=-1001873697425, text=msg.text, reply_to_message_id=3)
            else:
                await bot.send_message(msg.from_user.id, "Вы получили слишком много предпреждений и были забанены")
        else:
            await bot.send_message(msg.from_user.id, "Ваш комментарий слишком длинный!")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(cmd_rules, commands=['rules'])
    dp.register_message_handler(get_message, content_types=['text'])
