import aiohttp
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup


# GWP provider settings
# TODO: divide providers into different modules, unify scrapping and parsing

TYPE = 'water'
ROOT_URL = 'https://www.gwp.ge'
URLS = [
    {"url": urljoin(ROOT_URL, '/ka/dagegmili'), "emergency": False},
    {"url": urljoin(ROOT_URL, '/ka/gadaudebeli'), "emergency": True}
]


# GWP provider scraper and parser

async def collect_outages() -> list:
    """Wrapper"""

    notifications = await scrap_notifications()
    outages = await parse_notifications_info(notifications)
    return outages


async def request_soup(url: str) -> BeautifulSoup:
    """Returns soup from given url"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_text = await response.text()

    soup = BeautifulSoup(response_text, 'html.parser')
    return soup


async def scrap_notifications() -> list:
    """Scraps notifications based on their type from webpage"""

    notifications = []

    for item in URLS:
        url = item.get("url")
        emergency = item.get("emergency")
        soup = await request_soup(url)
        outages_table = soup.find("table", {"class": "samushaoebi"})
        outages_blocks = outages_table.find_all('tr')

        for item in outages_blocks:
            date = datetime.strptime(item.find("span", {"style": "color:#f00000"}).text, "%d/%m/%Y")

            if date >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                title = item.find_all("a")[1].get_text(strip=True)
                link = urljoin(ROOT_URL, item.a.get("href"))
                notifications.append(
                    {
                        "type": TYPE,
                        "date": date,
                        "title": title,
                        "emergency": emergency,
                        "link": link,
                    }
                )

    return notifications


async def parse_notifications_info(notifications: list) -> list:  # noqa: C901
    """Parses info from notifications"""

    notifications_info = []

    for notification in notifications:

        url = notification.get('link')
        soup = await request_soup(url)

        type = notification.get("type")
        date = notification.get('date')
        title = notification.get('title')

        emergency = notification.get("emergency")

        # For emergency outages
        if emergency:
            outage_text = soup.css.select(".initial > ul > li > p")
            for i in outage_text:
                if i.get_text(strip=True) != '':
                    info = i.get_text(strip=True).replace("\xa0", " ")
                    notifications_info.append(
                        {
                            'date': date,
                            'type': type,
                            'emergency': emergency,
                            'title': title,
                            'info': info
                        }
                    )
        # For planned outages
        else:
            outage_text = soup.css.select(".news-details > p")
            temp = []
            for i in outage_text:
                if i.get_text(strip=True) != '':
                    temp.append(i.get_text(strip=True).replace("\xa0", " "))

            info = "".join(temp[1:-2])
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
