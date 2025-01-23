from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def load_cookies():
    cookies = []
    with open('parsers/cookies.txt', 'r') as f:
        cookie_data = f.read().split(';')

        for cookie in cookie_data:
            cookie = cookie.strip()
            if '=' in cookie:
                name, value = cookie.split('=', 1)
                cookies.append({
                    'name': name,
                    'value': value,
                    'path': '/',
                    'domain': '.dns-shop.ru'
                })
    return cookies


def fetch_smartphones_from_dns():
    base_url = "https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?p="
    page_number = 1
    max_pages = 15 # Сколько всего страниц будем парсить
    data = []  # Список для хранения результатов

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel='chrome')
        context = browser.new_context()

        # Загружаем куки и добавляем их в контекст
        cookies = load_cookies()
        context.add_cookies(cookies)

        page = context.new_page()

        while page_number <= max_pages:
            url = f"{base_url}{page_number}"

            # Переход на страницу
            response = page.goto(url, wait_until="domcontentloaded")

            if response.status != 200:
                print(f"Ошибка при загрузке страницы: {response.status}.\nОбновите cookies")
                break

            page.wait_for_selector('.product-buy__price', timeout=5000)

            # Получаем карточки продуктов
            product_cards = page.query_selector_all(".catalog-product.ui-button-widget")

            # Перебираем все карточки и выводим их HTML
            for card in product_cards:
                card_html = card.inner_html()

                soup = BeautifulSoup(card_html, 'html.parser')

                # Извлекаем название товара
                name_element = soup.find("a", class_="catalog-product__name")
                name = name_element.text.strip() if name_element else "Нет названия"

                # Извлекаем цену товара
                price_element = soup.find("div", class_="product-buy__price product-buy__price_active")
                if price_element:
                    # Удаляем содержимое тега <span> (предыдущая цена)
                    for span in price_element.find_all("span"):
                        span.extract()
                        price = price_element.text.strip()
                else:
                    # Если активной цены нет, берём стандартную цену
                    default_price_element = soup.find("div", class_="product-buy__price")
                    price = default_price_element.text.strip() if default_price_element else "Нет цены"

                # Сохраняем данные в список
                data.append({
                    "name": name,
                    "price": price
                })

            page_number += 1

        browser.close()
        return data