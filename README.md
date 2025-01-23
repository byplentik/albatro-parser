## Описание проекта

Этот проект представляет собой набор парсеров для сайтов DNS-Shop и M.Video, которые извлекают информацию о товарах (в частности, смартфонах) и сохраняют данные в формате CSV или XLSX. Проект включает функции сортировки товаров и настройки выходных данных.

> **Важно:** Для работы парсера DNS необходимо загрузить cookies из вашего браузера. Без этого скрипт не сможет корректно функционировать.

## Структура проекта

```
project/
|-- main.py
|-- utils/
|   |-- save_to_csv_and_xls.py
|-- parsers/
    |-- dns_parser.py
    |-- mvideo_parser.py
```

### Файлы и директории
- **`main.py`**: Главный файл для запуска парсеров через командную строку.
- **`utils/save_to_csv_and_xls.py`**: Утилита для сохранения данных в формате CSV или XLSX.
- **`parsers/dns_parser.py`**: Парсер для сайта DNS.
- **`parsers/mvideo_parser.py`**: Парсер для сайта M.Video.

## Установка и запуск

### 1. Установка зависимостей

Для работы проекта необходим Python версии 3.8 и выше. Установите зависимости с помощью pip:

```bash
pip install -r requirements.txt
```

Пример содержимого `requirements.txt`:
```plaintext
playwright
beautifulsoup4
requests
openpyxl
```

### 2. Инициализация Playwright
Перед запуском парсера DNS выполните команду для установки браузеров Playwright:

```bash
playwright install
```

### 3. Получение cookies для DNS

1. Откройте сайт DNS (https://www.dns-shop.ru) в вашем браузере.
2. Включите инструменты разработчика (обычно нажатием `F12`).
3. Найдите вкладку "Application" или "Storage".
4. Скопируйте cookies и сохраните их в файл `cookies.txt` в корне проекта. Формат файла:

```
name=value; name2=value2; ...
```

### 4. Запуск парсеров

#### Аргументы командной строки

- `parser`: Выбор парсера (`dns` или `mvideo`).
- `-f`, `--format`: Формат сохранения данных (`csv` или `xlsx`).
- `-o`, `--output`: Имя файла для сохранения данных (без расширения). По умолчанию: `products`.
- `-s`, `--sort`: Порядок сортировки (`asc` или `desc`). По умолчанию: `asc`.

#### Примеры команд

1. Запуск парсера DNS:

```bash
python main.py dns -f csv -o dns_products -s asc
```

2. Запуск парсера M.Video:

```bash
python main.py mvideo -f xlsx -o mvideo_products -s desc
```

## Дополнительная информация

### Функции

#### 1. `fetch_smartphones_from_dns()` (dns_parser.py)
- Собирает данные о смартфонах с сайта DNS.
- Работает через библиотеку Playwright и BeautifulSoup.

#### 2. `fetch_all_product_ids()` (mvideo_parser.py)
- Получает список идентификаторов продуктов из категории M.Video через API.

#### 3. `save_to_csv_and_xls()` (save_to_csv_and_xls.py)
- Сохраняет данные в формат CSV и/или XLSX.

### Возможные ошибки и их решения
