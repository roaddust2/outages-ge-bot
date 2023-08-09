import requests
from datetime import datetime
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from settings import translator


# GWP provider settings
# TODO: divide providers into different modules, unify scrapping and parsing
# TODO: Unite planned and emergecy parsers

ROOT_URL = 'https://www.gwp.ge'
PLANNED_URL = urljoin(ROOT_URL, '/en/dagegmili')
EMERGENCY_URL = urljoin(ROOT_URL, '/en/gadaudebeli')


def scrap_notifications(type: str) -> list:
    '''
    Scraps notifications based on their type from webpage

        Parameters:
            type (str): String specifies type of outage:
                'planned' or 'emergency'

        Returns:
            notifications (list): A list of notifications, each packed in dict:
                [{
                    'date': '2023-07-18',
                    'title': 'Title',
                    'link': 'https://example.com',
                }]
    '''

    _map = {
        'planned': PLANNED_URL,
        'emergency': EMERGENCY_URL,
    }

    notifications = []

    response = requests.get(_map.get(type))
    soup = BeautifulSoup(response.content, 'html.parser')

    outages_table = soup.find("table", {"class": "samushaoebi"})
    outages_blocks = outages_table.find_all('tr')

    for item in outages_blocks:
        date_obj = datetime.strptime(item.find("span", {"style": "color:#f00000"}).text, "%d/%m/%Y")
        date_str = date_obj.strftime("%Y-%m-%d")
        title = item.find_all("a")[1].get_text(strip=True)
        link = urljoin(ROOT_URL, item.a.get("href"))
        if date_obj >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
            notifications.append(
                {
                    'date': date_str,
                    'title': title,
                    'link': link,
                }
            )

    return notifications


def parse_planned_notifications_info(notifications: list) -> list:
    '''
    Parses info from planned notifications

        Parameters:
            notifications (list): A list of notifications, each packed in dict:
                [{
                    'date': '2023-07-18',
                    'title': 'Title',
                    'link': 'https://example.com',
                }]

        Returns:
            notifications_info (list): A list of notifications info, each packed in dict:
                [{
                    'date': '2023-07-18',
                    'type': 'water',
                    'emergency': False,
                    'geo_title': 'Title',
                    'en_title': 'Title',
                    'geo_info': 'Info',
                    'en_info': 'Info',
                }]
    '''

    notifications_info = []

    for notification in notifications:
        response = requests.get(notification.get('link'))
        soup = BeautifulSoup(response.content, 'html.parser')
        outage_text = soup.css.select(".news-details > p")
        type = 'water'
        emergency = False
        date = notification.get('date')
        geo_title = notification.get('title')
        en_title = translator.translate(geo_title)

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


def parse_emergency_notifications_info(notifications: list) -> list:
    '''
    Parses info from emergency notifications

        Parameters:
            notifications (list): A list of notifications, each packed in dict:
                [{
                    'date': '2023-07-18',
                    'title': 'Title',
                    'link': 'https://example.com',
                }]

        Returns:
            notifications_info (list): A list of notifications info, each packed in dict:
                [{
                    'date': '2023-07-18',
                    'type': 'water',
                    'emergency': True,
                    'geo_title': 'Title',
                    'en_title': 'Title',
                    'geo_info': 'Info',
                    'en_info': 'Info',
                }]
    '''

    notifications_info = []

    for notification in notifications:
        response = requests.get(notification.get('link'))
        soup = BeautifulSoup(response.content, 'html.parser')
        outage_text = soup.css.select(".initial > ul > li > p")
        type = 'water'
        emergency = True
        date = notification.get('date')
        geo_title = notification.get('title')
        en_title = translator.translate(geo_title)
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

    return notifications_info
