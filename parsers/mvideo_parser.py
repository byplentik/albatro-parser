import requests
import statistics


def fetch_all_product_ids(category_id):
    """Функция для получения всех productIds конкретной категории из API."""
    base_url = "https://www.mvideo.ru/bff/products/v2/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    params = {
        "categoryIds": category_id,
        "offset": 0,
        "limit": 1000,
        "filterParams": "WyJ0b2xrby12LW5hbGljaGlpIiwiIiwiZGEiXQ%3D%3D",
        "doTranslit": "true",
    }

    cookies = {
        "MVID_CITY_ID": "CityCZ_975",
        "MVID_REGION_ID": "1",
        "MVID_REGION_SHOP": "S002",
        "MVID_TIMEZONE_OFFSET": "3",
    }

    # Отправляем запрос
    response = requests.get(base_url, headers=headers, params=params, cookies=cookies)
    if response.status_code != 200:
        print(f"Ошибка {response.status_code}: {response.text}")
        raise Exception

    data = response.json()
    product_ids = data['body']['products']

    return product_ids


def fetch_product_details(product_ids):
    """Функция для получения деталей товаров по их ID."""
    base_url = "https://www.mvideo.ru/bff/product-details/list"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "origin": "https://www.mvideo.ru",
        "referer": "https://www.mvideo.ru/",
    }

    payload = {
        "brand": True,
        "category": True,
        "mediaTypes": ["images"],
        "productIds": product_ids,
        "propertiesConfig": {"propertiesPortionSize": 5},
        "propertyTypes": ["KEY"],
        "status": True,
    }

    cookies = {
        "MVID_CITY_ID": "CityCZ_975",
        "MVID_REGION_ID": "1",
        "MVID_REGION_SHOP": "S002",
        "MVID_TIMEZONE_OFFSET": "3",
    }

    response = requests.post(base_url, headers=headers, json=payload, cookies=cookies)
    if response.status_code != 200:
        print(f"Ошибка {response.status_code}: {response.text}")
        return None

    data = response.json()
    products = data.get("body", {}).get("products", [])

    return products


def fetch_product_prices(product_ids):
    """Функция для получения цен товаров."""
    base_url = "https://www.mvideo.ru/bff/products/prices"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "origin": "https://www.mvideo.ru",
        "referer": "https://www.mvideo.ru/",
    }

    params = {
        "productIds": ",".join(product_ids),
    }

    cookies = {
        "MVID_CITY_ID": "CityCZ_975",
        "MVID_REGION_ID": "1",
        "MVID_REGION_SHOP": "S002",
        "MVID_TIMEZONE_OFFSET": "3",
    }

    response = requests.get(base_url, headers=headers, params=params, cookies=cookies)
    if response.status_code != 200:
        print(f"Ошибка {response.status_code}: {response.text}")
        return None

    data = response.json()
    prices = data.get("body", {}).get("materialPrices", [])
    return {price["productId"]: price["price"]["salePrice"] for price in prices}

