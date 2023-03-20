import asyncio
from aiogram import executor
from create_bot import dp
from bot_source.handlers import client
import infinity_polling


async def on_startup(_):
    print('Bot is online')
    asyncio.create_task(infinity_polling.check_database())


async def on_shutdown(_):
    print('Bot is going off')



client.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)


