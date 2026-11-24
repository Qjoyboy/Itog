import logging

import requests

logger = logging.getLogger("etl")

def fetch_data(start, end):
    api_url = "https://api.itresume.ru/statistics/"

    params = {
        "client": "Skillfactory",
        "client_key": "M2MGWS",
        "start": start,
        "end": end
    }
    logger.info("Starting data extraction")
    response = requests.get(
        api_url,
        params=params
    )
    if response.status_code != 200:
        raise response.raise_for_status()

    data = response.json()
    logger.info("API response type: %s", type(data).__name__)
    logger.info("API response preview: %s", str(data)[:1000])
    if not isinstance(data, list):
        raise ValueError("Не список ")
    logger.info("Data extraction completed: %s records", len(data))
    return data 