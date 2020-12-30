import json
import time

import requests
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

api_key = '23bc8a4f-d917-4fae-b9ea-204fc374faa6'  # Private key. Change for your own use
iftt_key = 'k8hQV5_tTZR4n_cOOF2F8vWxCV5utvUdPwfvQ1HSOol'  # Private key. Change for your own use
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/Crypto_price_notifications/with/key' \
                    '/k8hQV5_tTZR4n_cOOF2F8vWxCV5utvUdPwfvQ1HSOol '
amount = 10  # Set this value to what you want to be notified about
symbol = 'BTC'  # Interchangeable ticker symbol. Change to any valid value


def get_latest_price(ticker: str) -> float:
    """
    Search Coinmarketcap's database for the current price of the desire currency
    """
    parameters = {
        'symbol': ticker
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        price = data['data'][symbol]['quote']['USD']['price']
        return price
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def notify(event: str, coin: str, value: float) -> None:
    """
    Send a request to the IFTTT application to trigger a notification
    """
    data = {'value1': coin, 'value2': value}
    ifttt_event_url = ifttt_webhook_url.format(event)
    requests.post(ifttt_event_url, json=data)


def main() -> None:
    """
    Main loop. Checks to see if the price of <symbol> is greater than <amount> and send a notification if so
    """
    while True:
        price = get_latest_price(symbol)
        if price > amount:
            notify('Crypto_price_notifications', symbol, amount)
        time.sleep(30)


if __name__ == '__main__':
    main()
