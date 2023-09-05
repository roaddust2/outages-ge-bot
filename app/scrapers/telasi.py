import aiohttp
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from app.scrapers.base import AbstractProvider


class Telasi(AbstractProvider):
    """Telasi electricity provider class"""

    TYPE = 'electricity'
    ROOT_URL = 'http://www.telasi.ge'
    URL = urljoin(ROOT_URL, '/ru/power')

    async def get_localized_url(self, url: str) -> str:
        """Get localized url in 'ge' locale"""

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_text = await response.text()

        soup = BeautifulSoup(response_text, 'html.parser')
        link = soup.find('a', string="Geo").get("href")
        return urljoin(self.ROOT_URL, link)

    def normalize_date(self, date: str) -> str:
        normalized = date[0:10].replace(" ", ".")
        return normalized

    def get_title(self, soup: BeautifulSoup) -> str:
        strong_tags = soup.css.select(".field-item > h3 > strong")
        if strong_tags:
            title = [strong.get_text(strip=True).replace("\xa0", " ") for strong in strong_tags]
            return ' '.join(title)
        p_tag = soup.css.select_one(".field-item > p[align=\"center\"]")
        if p_tag:
            return p_tag.get_text(strip=True).replace("\xa0", " ")
        else:
            return ""

    def get_info(self, soup: BeautifulSoup) -> str:
        p_tags = soup.css.select(".field-item > p")
        if p_tags:
            info = [p.get_text(strip=True).replace("\xa0", " ") for p in p_tags][:-1]
            return ' '.join(info)
        return ""

    async def scrap_notifications(self) -> list:
        """Scraps notifications from webpage"""

        notifications = []

        url = await self.get_localized_url(self.URL)
        soup = await self.request_soup(url)
        outages_blocks = soup.css.select(".power-submenu > ul > li > a")

        for outage in outages_blocks:
            outage_string = outage.string.strip()
            date = datetime.strptime(self.normalize_date(outage_string), "%d.%m.%Y")
            current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if date >= current_date:
                title = outage_string[13:]
                link = urljoin(self.ROOT_URL, outage.get("href"))
                notifications.append(
                    {
                        "type": self.TYPE,
                        "date": date.strftime("%Y-%m-%d"),
                        "title": title,
                        "emergency": True if "არაგეგმიური" in title else False,
                        "link": link,
                    }
                )

        return notifications

    async def parse_notifications_info(self, notifications: list) -> list:
        """Parses info from notifications"""

        notifications_info = []

        for notification in notifications:

            url = notification.get('link')
            soup = await self.request_soup(url)
            date = notification.get('date')
            type = notification.get("type")
            emergency = notification.get("emergency")
            title = self.get_title(soup)
            info = self.get_info(soup)

            notifications_info.append(
                {
                    'date': date,
                    'type': type,
                    'emergency': emergency,
                    'title': title,
                    'info': info
                }
            )

        return notifications_info
