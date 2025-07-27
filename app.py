from aiogram import Bot, Dispatcher
import asyncio

from database.engine import session_maker, create_db
from middleware import DataBaseSession
from routers import private_router

token = "7633093312:AAFcgT9nK-1yAUMNusnlCdpo9elgpx4kP2w"

bot = Bot(token=token)
dp = Dispatcher()
dp.include_router(private_router)

async def on_startup(bot):
    await create_db()

async def on_shutdwon(bot):
    print("Bot shut up")

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdwon)


    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())