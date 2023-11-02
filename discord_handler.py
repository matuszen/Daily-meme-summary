import discord
import logging as log
from dc_token import TOKEN, CHANNEL_ID


class DiscordHandler:
    async def __init__(self) -> None:
        self.client = discord.Client()

        try:
            await self.client.login(TOKEN)
            await self.client.connect()

            self.channel = self.client.get_channel(CHANNEL_ID)

            if self.channel is None:
                log.error("Channel object is None")

        except discord.LoginFailure as e:
            log.error(f"Login failed: {e}")

        else:
            log.info("Succesfully login into bot")

        finally:
            await self.client.close()
            log.error("There was a problem with setting channel")

    async def send(self, memes) -> None:
        try:
            for meme in memes:
                await self.channel.send(file=discord.File(meme))

        except discord.HTTPException as e:
            log.error(f"There was an HTTP error while sending memes: {e}")

        else:
            log.info("Succesfully sended memes")

        finally:
            await self.client.close()
            log.error("There was a problem with sending memes")
