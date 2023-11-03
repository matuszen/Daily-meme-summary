import os
import discord
import logging as log
from discord.ext import commands

from DiscordHandler.dc_token import TOKEN, CHANNEL_ID


class DiscordHandler:
    def __init__(self) -> None:
        self._bot: commands.Bot
        self._channel: discord.Thread

    async def run(self) -> None:
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False
        intents.messages = True

        self._bot = commands.Bot(
            description="meme-summary",
            command_prefix="***",
            self_bot=True,
            intents=intents,
        )

        @self._bot.event
        async def on_ready():
            log.info(
                f"Succesfully logged as `{self._bot.user.name}` #{self._bot.user.discriminator}, ID: {self._bot.user.id}"
            )

            self._channel = self._bot.get_channel(CHANNEL_ID)

            if self._channel is None:
                log.error("Channel not found")
                exit()

            log.info(f"Connected to channel: `{self._channel}`")

            await self._send()

        await self._bot.start(TOKEN)

    async def _send(self) -> None:
        directory = os.path.join(
            os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1]), "cache"
        )

        files = [os.path.join(directory, file) for file in os.listdir(directory)]

        memes_count = 0

        for file in files:
            try:
                with open(file, "rb") as file:
                    await self._channel.send(file=discord.File(file))
                    memes_count += 1

            except discord.HTTPException as e:
                log.error(
                    f"There was an HTTP error while sending {memes_count} meme: {e}"
                )
                continue

            except Exception as e:
                log.error(f"Unknown error while sending {memes_count} meme: {e}")
                continue

        if memes_count != 0:
            log.info(f"Successfully sent {memes_count} memes")
        else:
            log.error(f"No meme was send")

        await self._bot.close()
