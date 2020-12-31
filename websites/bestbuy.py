#! /usr/bin/env python3

from requests import get

def check(item):
    result = get(item['url'], headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'})
    if result.status_code != 200:
        raise Exception(f"Bad status code: {result.status_code}")

    result_html = result.text.lower()

    if 'add to cart' in result_html:
        return True

    if 'sold out' in result_html:
        return False

    raise Exception("Add to cart button is missing or has unexpected text")
