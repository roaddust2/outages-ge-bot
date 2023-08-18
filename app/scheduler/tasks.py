from app.scrapers import gwp as GWP
from app.db.functions import select_addresses_by_cities


PROVIDER_INFO = {
    "GWP": {
        "cities": ["tbilisi"],
        "planned": True,
        "emergency": True,
    },
}


def get_provider_info(provider: str) -> dict:
    return PROVIDER_INFO[provider]


def collect_addresses_with_outages(provider: str) -> list:

    result = []
    outages = []

    provider_info = get_provider_info(provider)

    if provider_info.get("planned"):
        planned_notifications = GWP.scrap_notifications("planned")
        outages.extend(GWP.parse_planned_notifications_info(planned_notifications))

    if provider_info.get("emergency"):
        emergency_notifications = GWP.scrap_notifications("emergency")
        outages.extend(GWP.parse_emergency_notifications_info(emergency_notifications))

    addresses = select_addresses_by_cities(provider_info.get("cities"))

    for address in addresses:
        for outage in outages:
            geo_info = outage.get("geo_info").lower()
            en_info = outage.get("en_info").lower()
            if address.street.lower() in geo_info or address.street.lower() in en_info:
                result.append({address: outage})

    return result
