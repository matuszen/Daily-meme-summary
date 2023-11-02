import logging as log
import asyncio

from WebCollector import WebCollector
from DiscordHandler import DiscordHandler
from MediaDownloader import MediaDownloader


def main() -> None:
    # urls = WebCollector().all()

    # print(urls)

    # MediaDownloader(urls).download()

    discord = DiscordHandler()
    asyncio.run(discord.connect())


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        log.error("Keyboard Interrupt")
        exit()
