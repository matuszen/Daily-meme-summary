import logging as log
import asyncio

from WebCollector import WebCollector
from DiscordHandler import DiscordHandler
from MediaDownloader import MediaDownloader

from utils import get_network_usage

log.basicConfig(level=log.INFO, format="[%(levelname)s] %(name)s: %(message)s")


async def main() -> None:
    urls = WebCollector().all()
    media = MediaDownloader(urls)
    discord = DiscordHandler()

    media.download()

    await discord.run()

    media.clear_cache()


if __name__ == "__main__":
    try:
        bytes_sent_before, bytes_recv_before = get_network_usage()
        asyncio.run(main())
        bytes_sent_after, bytes_recv_after = get_network_usage()

        bytes_sent_diff = bytes_sent_after - bytes_sent_before
        bytes_recv_diff = bytes_recv_after - bytes_recv_before

        log.info(f"Data sent: {bytes_sent_diff} bytes")
        log.info(f"Data received: {bytes_recv_diff} bytes")

    except KeyboardInterrupt:
        bytes_sent_after, bytes_recv_after = get_network_usage()

        bytes_sent_diff = bytes_sent_after - bytes_sent_before
        bytes_recv_diff = bytes_recv_after - bytes_recv_before

        log.error("Keyboard Interrupt")

        log.info(f"Data sent: {bytes_sent_diff} bytes")
        log.info(f"Data received: {bytes_recv_diff} bytes")

        exit()

    except Exception as e:
        log.error(f"Unexpected error: {e}")

        exit()
