import requests
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup


TYPE = 'electricity'
ROOT_URL = 'http://www.telasi.ge'
URL = urljoin(ROOT_URL, '/ru/power')


def collect_outages() -> list:
    """Wrapper"""

    outages = parse_notifications_info(scrap_notifications())
    return outages


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


def normalize_date(date: str) -> str:
    normalized = date[0:10].replace(" ", ".")
    return normalized


def get_title(soup):
    strong_tags = soup.css.select(".field-item > h3 > strong")
    if strong_tags:
        title = [strong.get_text(strip=True).replace("\xa0", " ") for strong in strong_tags]
        return ' '.join(title)
    p_tag = soup.css.select_one(".field-item > p[align=\"center\"]")
    return p_tag.get_text(strip=True).replace("\xa0", " ")


def get_info(soup):
    p_tags = soup.css.select(".field-item > p")
    if p_tags:
        info = [p.get_text(strip=True).replace("\xa0", " ") for p in p_tags][:-1]
        return ' '.join(info)
    return ""


def scrap_notifications() -> list:
    """Scraps notifications from webpage"""

    notifications = []

    url = get_localized_url(URL)
    soup = request_soup(url)
    outages_blocks = soup.css.select(".power-submenu > ul > li > a")

    for outage in outages_blocks:
        outage_string = outage.string.strip()
        date = datetime.strptime(normalize_date(outage_string), "%d.%m.%Y")
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if date >= current_date:
            title = outage_string[13:]
            link = urljoin(ROOT_URL, outage.get("href"))
            notifications.append(
                {
                    "type": TYPE,
                    "date": date,
                    "title": title,
                    "emergency": True if "არაგეგმიური" in title else False,
                    "link": link,
                }
            )

    return notifications


def parse_notifications_info(notifications: list) -> list:
    """Parses info from notifications"""

    notifications_info = []

    for notification in notifications:

        url = notification.get('link')
        soup = request_soup(url)
        date = notification.get('date')
        type = notification.get("type")
        emergency = notification.get("emergency")
        title = get_title(soup)
        info = get_info(soup)

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
