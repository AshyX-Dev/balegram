from balegram import AsyncClient
from balegram.types import Message
import asyncio

token = ""
bot = AsyncClient(token)

@bot.on('message')
async def onMessage(message: Message):
    await message.asyncReply("Hello World")
    await message.asyncReplyPhoto("./photo.jpg", "Hiii") # or URL Photo
    # Location - Video - Document - Audio - Animation
    # Contact - Voice
    #
    # For sync, use reply - replyPhoto and ...

asyncio.run(bot.run()) # Run Decorator