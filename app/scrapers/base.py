import logging
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class AbstractProvider:
    """Provider abstract class"""

    TYPE = 'type'
    ROOT_URL = 'https://www.example.com'
    URLS = [
        {"url": urljoin(ROOT_URL, '/planned'), "emergency": False},
        {"url": urljoin(ROOT_URL, '/emergency'), "emergency": True}
    ]

    def __init__(self) -> None:
        pass

    async def collect_outages(self) -> list:
        """Wrapper"""

        try:
            notifications = await self.scrap_notifications()
            outages = await self.parse_notifications_info(notifications)
        except Exception as err:
            logging.error(f"Error occured while parsing, {err}")
        return outages

    async def request_soup(self, url: str) -> BeautifulSoup:
        """Returns soup from given url"""

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_text = await response.text()

        soup = BeautifulSoup(response_text, 'html.parser')
        return soup

    async def scrap_notifications(self) -> list:
        """Scraps notifications based on their type from webpage"""
        return []

    async def parse_notifications_info(self, notifications: list) -> list:
        """Parses info from notifications"""
        return []
