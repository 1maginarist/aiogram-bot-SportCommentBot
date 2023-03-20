import sqlite3
import asyncio
import datetime
import aiogram.utils.exceptions
from create_bot import bot
from aiogram.types import ChatPermissions

async def insert_comment(msg, mod_msg):

    # connecting to database
    conn = sqlite3.connect("bot_source/database/comment_db.db")
    c = conn.cursor()

    c.execute("INSERT INTO comments (time, id, comment) VALUES (?, ?, ?)", (datetime.datetime.now(), msg.from_user.id, mod_msg))

    conn.commit()
    conn.close()


async def insert_new_user(msg):
    conn = sqlite3.connect(r"bot_source/database/user_restrict_db.db")
    c = conn.cursor()

    c.execute("INSERT INTO RESTRICT (id, count) VALUES (?, ?)", (msg.from_user.id, 0))

    conn.commit()
    conn.close()


'''async def unban_user(user_id: int, unban_time: datetime.datetime):
    await asyncio.sleep((unban_time - datetime.datetime.now()).total_seconds())
    await bot.unban_chat_member(chat_id=user_id, user_id=user_id)'''


async def ban_user(user_id: int):
    pass
    #ban_duration = datetime.timedelta(days=7)
    #ban_time = datetime.datetime.now() + ban_duration
    #permissions = ChatPermissions(can_send_messages=False)
    #try:
    #    await bot.restrict_chat_member(chat_id=user_id, user_id=user_id, permissions=permissions, until_date=ban_time.timestamp())
    #except aiogram.utils.exceptions.BadRequest as e:
    #    print(f"Error: {e}")


def increase_count(msg):
    conn = sqlite3.connect(r"bot_source/database/user_restrict_db.db")
    c = conn.cursor()

    c.execute("UPDATE RESTRICT SET count = count + 1 WHERE id=?", (msg.from_user.id,))

    conn.commit()
    conn.close()


def check_for_ban(msg):
    conn = sqlite3.connect(r"bot_source/database/user_restrict_db.db")
    c = conn.cursor()

    c.execute("SELECT count FROM RESTRICT WHERE id=?", (msg.from_user.id,))
    count = c.fetchone()[0]

    conn.commit()
    conn.close()

    if count >= 5:
        return False
    else:
        return True
