import asyncio
import logging
import sqlite3
from create_bot import bot

conn = sqlite3.connect("bot_source/database/comment_db.db")
c = conn.cursor()

async def send_data_to_bot(comment):
    try:
        message = await bot.send_message(chat_id=-1001873697425, text=comment, reply_to_message_id=151)
        await asyncio.sleep(30)
        await message.delete()
    except Exception as e:
        logging.error(f'Failed to send comment: {e}')


async def check_database():
    while True:
        c.execute('''SELECT * FROM comments ORDER By time ASC LIMIT 1''')
        row = c.fetchone()
        if row:
            comment = f"<b>{row[2]}</b>"
            c.execute('''DELETE FROM comments WHERE time=?''', (row[0],))
            conn.commit()
            c.execute('''VACUUM''')
            conn.commit()

            await send_data_to_bot(comment)

        else:
            await asyncio.sleep(3)
