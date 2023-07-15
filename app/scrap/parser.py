from datetime import datetime
import requests
from bs4 import BeautifulSoup
import providers.gwp as GWP
from translate import Translator


translator = Translator(to_lang="en", from_lang='ka')


def current_datetime() -> datetime:
    """Return current date in datetime format"""

    output = datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return output


def parse_emergency_notifications() -> list:
    """Parse notifications from emergencies page"""

    notifications = []

    response = requests.get(GWP.EMERGENCY_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    outages_table = soup.find("table", {"class": "samushaoebi"})
    outages_blocks = outages_table.find_all('tr')

    for item in outages_blocks:
        _date_obj = datetime.strptime(item.find("span", {"style": "color:#f00000"}).text, "%d/%m/%Y")
        _date_str = _date_obj.strftime("%Y-%m-%d")
        _title = item.find_all("a")[1].get_text(strip=True)
        _link = f'{GWP.ROOT_URL}{item.a.get("href")}'
        if _date_obj >= current_datetime():
            notifications.append(
                {
                    'date': _date_str,
                    'title': _title,
                    'link': _link
                }
            )

    return notifications


def parse_notifications_info(notifications: list) -> list:
    """Parse info from notifications"""

    notifications_info = []

    for notification in notifications:
        response = requests.get(notification.get('link'))
        soup = BeautifulSoup(response.content, 'html.parser')
        outage_text = soup.css.select(".initial > ul > li > p")
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
                        'geo_title': geo_title,
                        'en_title': en_title,
                        'geo_info': geo_info,
                        'en_info': en_info,
                    }
                )

    return notifications_info


print(parse_notifications_info(parse_emergency_notifications()))
