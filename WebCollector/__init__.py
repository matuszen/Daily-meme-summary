import requests
import logging as log
from bs4 import BeautifulSoup, element
from datetime import datetime, timedelta

from WebCollector.urls import WEBSITES


class WebCollector:
    def __init__(self) -> None:
        self._webpages_urls = WEBSITES
        self._media_urls = set()
        self._media_count = 0

        self._today = datetime.today()
        self._today = datetime(
            self._today.year, self._today.month, self._today.day, 0, 0, 0
        )
        self._yesterday = self._today - timedelta(days=1)

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

                if self._yesterday <= posted_datetime <= self._today:
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

    def _demotywatory(self) -> None:
        subpage = 1

        last_subpage = False
        should_continue = True

        def convert_month_to_number(month_name: str) -> int:
            polish_months = {
                "stycznia": 1,
                "lutego": 2,
                "marca": 3,
                "kwietnia": 4,
                "maja": 5,
                "czerwca": 6,
                "lipca": 7,
                "sierpnia": 8,
                "września": 9,
                "października": 10,
                "listopada": 11,
                "grudnia": 12,
            }

            return polish_months.get(month_name)

        while should_continue:
            if last_subpage:
                should_continue = False

            URL = f"{self._webpages_urls['DEMOTYWATORY'][f'MAIN_URL']}{subpage}"
            MEDIA_URL = self._webpages_urls["DEMOTYWATORY"]["MEDIA_URL"]

            response = requests.get(URL)

            soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
            articles: list[element.Tag] = (
                soup.find("div", id="main_container")
                .find("section", class_="demots")
                .find_all("article")
            )

            for article in articles:
                posted_time = article.find("time")

                if posted_time is None:
                    continue

                date_parts = posted_time.get_text().split()
                day = int(date_parts[0])
                month = convert_month_to_number(date_parts[1])
                year = int(date_parts[2])
                time = date_parts[4]

                formatted_date_str = f"{day:02d}-{month:02d}-{year} o {time}"

                posted_datetime = datetime.strptime(
                    formatted_date_str, "%d-%m-%Y o %H:%M"
                )

                if self._yesterday <= posted_datetime <= self._today:
                    images: list[element.Tag] = article.find_all("img")

                    for image in images:
                        image_url = image.get("src")
                        if image_url and image_url.startswith(MEDIA_URL):
                            self._media_urls.add(image_url)
                            self._media_count += 1

                    last_subpage = False

                else:
                    last_subpage = True

            subpage += 1

    def all(self) -> set[str]:
        log.info("Start collecting memes")

        self._jbzd()
        self._demotywatory()

        log.info(f"{self._media_count} memes finded")

        if self._media_count == 0:
            exit()

        return self._media_urls
