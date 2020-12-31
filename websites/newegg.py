#! /usr/bin/env python3

from requests import get

def check(item):
    result = get('https://www.newegg.com/product/api/ProductRealtime?ItemNumber={item_number}'.format(item_number=item['item_number'])).json()
    return result['MainItem']['Instock']
