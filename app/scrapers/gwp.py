import requests
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from settings import translator


# GWP provider settings
# TODO: divide providers into different modules, unify scrapping and parsing

TYPE = 'water'
ROOT_URL = 'https://www.gwp.ge'
URLS = [
    {"url": urljoin(ROOT_URL, '/en/dagegmili'), "emergency": False},
    {"url": urljoin(ROOT_URL, '/en/gadaudebeli'), "emergency": True}
]


# GWP provider scraper and parser

def request_soup(url: str) -> BeautifulSoup:
    """Returns soup from given url"""

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def scrap_notifications() -> list:
    """Scraps notifications based on their type from webpage"""

    notifications = []

    for item in URLS:
        url = item.get("url")
        emergency = item.get("emergency")
        soup = request_soup(url)
        outages_table = soup.find("table", {"class": "samushaoebi"})
        outages_blocks = outages_table.find_all('tr')

        for item in outages_blocks:
            date_obj = datetime.strptime(item.find("span", {"style": "color:#f00000"}).text, "%d/%m/%Y")

            if date_obj >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                date_str = date_obj.strftime("%Y-%m-%d")
                title = item.find_all("a")[1].get_text(strip=True)
                link = urljoin(ROOT_URL, item.a.get("href"))
                notifications.append(
                    {
                        "type": TYPE,
                        "date": date_str,
                        "title": title,
                        "emergency": emergency,
                        "link": link,
                    }
                )

    return notifications


def parse_notifications_info(notifications: list) -> list:  # noqa: C901
    """Parses info from notifications"""

    notifications_info = []

    for notification in notifications:

        url = notification.get('link')
        soup = request_soup(url)

        type = notification.get("type")
        date = notification.get('date')
        geo_title = notification.get('title')
        en_title = translator.translate(geo_title)

        emergency = notification.get("emergency")

        # For emergency outages
        if emergency:
            outage_text = soup.css.select(".initial > ul > li > p")
            for i in outage_text:
                if i.get_text(strip=True) != '':
                    geo_info = i.get_text(strip=True).replace("\xa0", " ")
                    en_info = translator.translate(geo_info)
                    notifications_info.append(
                        {
                            'date': date,
                            'type': type,
                            'emergency': emergency,
                            'geo_title': geo_title,
                            'en_title': en_title,
                            'geo_info': geo_info,
                            'en_info': en_info,
                        }
                    )
        # For planned outages
        else:
            outage_text = soup.css.select(".news-details > p")
            info = []
            for i in outage_text:
                if i.get_text(strip=True) != '':
                    info.append(i.get_text(strip=True).replace("\xa0", " "))

            geo_info = "".join(info[1:-2])
            en_info = translator.translate(geo_info)
            notifications_info.append(
                {
                    'date': date,
                    'type': type,
                    'emergency': emergency,
                    'geo_title': geo_title,
                    'en_title': en_title,
                    'geo_info': geo_info,
                    'en_info': en_info,
                }
            )

    return notifications_info
