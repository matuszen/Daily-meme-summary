import os
import requests
from datetime import datetime


class MediaDownloader:
    def __init__(self, urls: set[str]) -> None:
        self._urls = urls

    def download(self) -> None:
        if not os.path.exists("cache"):
            os.makedirs("cache")

        for index, url in enumerate(self._urls, 1):
            response = requests.get(url)

            if response.status_code == 200:
                file_extension = url.split(".")[-1]
                today_date = datetime.now().strftime("%Y-%m-%d")
                filename = f"{today_date}_{index}.{file_extension}"
                file_path = os.path.join("cache", filename)

                with open(file_path, "wb") as file:
                    file.write(response.content)

                print(f"Downloaded file as {filename} to cache")
            else:
                print(f"Failed to download file from {url}")
