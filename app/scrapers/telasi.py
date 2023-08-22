import requests
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from settings import translator  # noqa: F401


TYPE = 'electricity'
ROOT_URL = 'http://www.telasi.ge'
URL = urljoin(ROOT_URL, '/ru/power')


def get_localized_url(url: str) -> str:
    """Get localized url in 'ge' locale"""

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    link = soup.find('a', string="Geo").get("href")
    return urljoin(ROOT_URL, link)


def request_soup(url: str) -> BeautifulSoup:
    """Returns soup from given url"""

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def scrap_notifications() -> list:
    """Scraps notifications from webpage"""

    notifications = []

    url = get_localized_url(URL)
    soup = request_soup(url)
    outages_blocks = soup.css.select(".power-submenu > ul > li > a")

    for outage in outages_blocks:
        outage_string = outage.string.strip()
        date_obj = datetime.strptime(outage_string[0:10], "%d.%m.%Y")
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if date_obj >= current_date:
            date_str = date_obj.strftime("%Y-%m-%d")
            title = outage_string[13:]
            link = urljoin(ROOT_URL, outage.get("href"))
            notifications.append(
                {
                    "type": TYPE,
                    "date": date_str,
                    "title": title,
                    "emergency": False,
                    "link": link,
                }
            )

    return notifications
