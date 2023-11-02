import logging as log
import asyncio

from WebCollector import WebCollector
from DiscordHandler import DiscordHandler
from MediaDownloader import MediaDownloader

log.basicConfig(level=log.INFO, format='[%(levelname)s] %(name)s: %(message)s')


async def main() -> None:
    # urls = WebCollector().all()

    # print(urls)

    # MediaDownloader(urls).download()

    discord = DiscordHandler()
    await discord.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        log.error("Keyboard Interrupt")
        exit()
