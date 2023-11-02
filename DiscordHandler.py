import discord
from discord.ext import commands
import os
import logging as log
from dc_token import TOKEN, CHANNEL_ID


class DiscordHandler():
    def __init__(self) -> None:
        pass
    
    async def run(self) -> None:
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False
        intents.messages = True
        
        self._bot = commands.Bot(
            description='meme-summary', command_prefix="***", self_bot=True, intents=intents
        )
        
        @self._bot.event
        async def on_ready():
            log.info(f'{self._bot.user.name}#{self._bot.user.discriminator} id: {self._bot.user.id}')

            self._channel = self._bot.get_channel(CHANNEL_ID)

            log.info(f'Connected to channel: {self._channel}')
            
            await self.send()

        await self._bot.start(TOKEN)
        await self._bot.close()
        
    async def send(self) -> None:        
        try:
            directory = os.path.join("/".join(os.path.abspath(__file__).split("/")[:-1]), "cache")
            files = [os.path.join(directory, file) for file in os.listdir(directory)].sort()
            
            print(files)
            
            for file in files:
                with open(file, "rb") as file:
                    await self._channel.send(file=discord.File(file))

        except discord.HTTPException as e:
            log.error(f"There was an HTTP error while sending memes: {e}")

        else:
            log.info("Successfully sent files")

        finally:
            log.error("There was a problem with sending files")

