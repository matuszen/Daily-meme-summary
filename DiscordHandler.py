import discord
from discord.ext import commands
import os
import logging as log
from dc_token import TOKEN, CHANNEL_ID


class DiscordHandler:
    def __init__(self) -> None:
        pass

    async def connect(self) -> None:
        intents = discord.Intents.default()
        # intents.typing = False
        # intents.presences = False

        self.client = commands.Bot(command_prefix="!", intents=intents)

        try:
            await self.client.login(TOKEN)
            await self.client.connect()

            self.channel = self.client.get_channel(CHANNEL_ID)

            if self.channel is None:
                log.error("Channel object is None")

        except discord.LoginFailure as e:
            log.error(f"Login failed: {e}")

        else:
            log.info("Successfully logged in to the bot")

    async def send(self) -> None:
        try:
            directory = "cache"
            files = [os.path.join(directory, file) for file in os.listdir(directory)]
            for file in files:
                with open(file, "rb") as file:
                    await self.channel.send(file=discord.File(file))

        except discord.HTTPException as e:
            log.error(f"There was an HTTP error while sending memes: {e}")

        else:
            log.info("Successfully sent files")

        finally:
            await self.client.close()
            log.error("There was a problem with sending files")
