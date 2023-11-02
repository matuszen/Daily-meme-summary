import requests
from datetime import datetime
from bs4 import BeautifulSoup, element
import logging as log

from . import urls


class WebCollector:
    def __init__(self) -> None:
        self._webpages_urls = urls.WEBSITES
        self._media_urls = set()
        self._media_count = 0

    def _jbzd(self) -> None:
        subpage = 1
        last_subpage = False
        should_continue = True

        while should_continue:
            if last_subpage:
                should_continue = False

            URL = f"{self._webpages_urls['JBZD'][f'MAIN_URL']}{subpage}"
            MEDIA_URL = self._webpages_urls["JBZD"]["MEDIA_URL"]

            response = requests.get(URL)

            soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
            articles: list[element.Tag] = soup.find_all("article", class_="article")

            for article in articles:
                article_time = article.find("span", class_="article-time")
                posted_time = article_time.get("data-date")
                posted_datetime = datetime.strptime(posted_time, "%Y-%m-%d %H:%M:%S")

                today = datetime.today()
                beginning_of_the_day = datetime(
                    today.year, today.month, today.day, 0, 0, 0
                )

                if posted_datetime >= beginning_of_the_day:
                    images: list[element.Tag] = article.find_all("img")
                    videos: list[element.Tag] = article.find_all("videoplyr")

                    for image in images:
                        image_url = image.get("src")
                        if (
                            image_url
                            and image_url.startswith(MEDIA_URL)
                            and "/normal/" in image_url
                        ):
                            self._media_urls.add(image_url)
                            self._media_count += 1

                    for video in videos:
                        video_url = video.get("video_url")
                        if video_url:
                            self._media_urls.add(video_url)
                            self._media_count += 1

                    last_subpage = False

                else:
                    last_subpage = True

            subpage += 1

    def all(self) -> set[str]:
        log.info("Start collecting memes")

        self._jbzd()

        log.info(f"{self._media_count} memes finded")

        return self._media_urls
