import asyncio
import logging
from aiogram import Bot, Dispatcher
from api.broker import broker
from db.session import async_session
from db.models import User
from sqlalchemy import select
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@broker.subscriber("code")
async def send_code(param: dict):
    username = param["username"]
    
    session = async_session()
    try:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if user:
            await bot.send_message(
                chat_id=username,
                text=f"Ваш код подтверждения: {user.code}"
            )
    finally:
        await session.close()
    
@broker.subscriber("success")
async def verify_success(param: dict):
    username = param["username"]
    message = param['message']
    await bot.send_message(
        chat_id=username,
        text=message
    )

async def main() -> None:
    async with broker:
        await broker.start()
        await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())