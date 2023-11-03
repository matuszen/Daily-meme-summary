import os
import requests
import logging as log
from datetime import datetime


class MediaDownloader:
    def __init__(self, urls: set[str]) -> None:
        self._urls = urls

    def download(self) -> None:
        if not os.path.exists("cache"):
            os.makedirs("cache")

        if os.listdir("cache") is not None:
            self.clear_cache()

        today_date = datetime.now().strftime("%d-%m-%Y")

        for index, url in enumerate(self._urls, 1):
            response = requests.get(url)

            if response.status_code == 200:
                file_extension = url.split(".")[-1]
                filename = f"{today_date}_{index}.{file_extension}"
                file_path = os.path.join("cache", filename)

                with open(file_path, "wb") as file:
                    file.write(response.content)

                log.info(f"Downloaded file as {filename} to cache")
            else:
                log.error(f"Failed to download file from {url}")

    def clear_cache(self) -> None:
        if not os.path.exists("cache"):
            os.makedirs("cache")

        else:
            for file_name in os.listdir("cache"):
                file_path = os.path.join("cache", file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    log.error(f"Failed to delete {file_path}. Reason: {e}")
