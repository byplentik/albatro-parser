import argparse

from parsers.dns_parser import fetch_smartphones_from_dns
from parsers.mvideo_parser import fetch_all_product_ids, fetch_product_details, fetch_product_prices
from utils.save_to_csv_and_xls import save_to_csv_and_xlsx


def run_dns_parser(output_format, output_filename, sort_order):
    print("Запуск парсера DNS...")

    # Получаем данные о смартфонах
    data = fetch_smartphones_from_dns()

    # Сортировка товаров
    print(f"Сортировка товаров в порядке: {sort_order}...")
    data.sort(key=lambda x: x["name"].lower(), reverse=(sort_order == "desc"))

    # Сохранение данных
    print(f"Сохранение данных в {output_format} формате...")
    if output_format == "csv":
        save_to_csv_and_xlsx(data, f"{output_filename}.csv", None)
    elif output_format == "xlsx":
        save_to_csv_and_xlsx(data, None, f"{output_filename}.xlsx")

    print("Данные успешно сохранены.")


def run_mvideo_parser(output_format, output_filename, sort_order):
    print("Запуск парсера M.Video...")
    category_id = 118  # Категория, для которой нужно получить товары

    # Получаем все productIds
    print("Получение списка товаров...")
    product_ids = fetch_all_product_ids(category_id)

    # Разделяем productIds на части по 50
    batch_size = 50
    product_details = []
    print("Загрузка данных товаров...")
    for i in range(0, len(product_ids), batch_size):
        batch = product_ids[i:i + batch_size]

        # Получаем детали товаров
        details = fetch_product_details(batch)

        # Получаем цены товаров
        prices = fetch_product_prices(batch)

        # Объединяем детали и цены
        for product in details:
            product_id = product["productId"]
            product_details.append({
                "productId": product_id,
                "name": product["name"],
                "salePrice": prices.get(product_id, "Цена отсутствует")
            })

    # Сортировка товаров
    print(f"Сортировка товаров в порядке: {sort_order}...")
    product_details.sort(key=lambda x: x["name"].lower(), reverse=(sort_order == "desc"))

    # Сохранение данных
    print(f"Сохранение данных в {output_format} формате...")
    if output_format == "csv":
        save_to_csv_and_xlsx(product_details, f"{output_filename}.csv", None)
    elif output_format == "xlsx":
        save_to_csv_and_xlsx(product_details, None, f"{output_filename}.xlsx")

    print("Данные успешно сохранены.")


def run_dns_parser(output_format, output_filename, sort_order):
    print("Запуск парсера DNS...")

    # Получаем данные о смартфонах
    data = fetch_smartphones_from_dns()
    if not data:
        print('Не работает :(')
        return

    # Сортировка товаров
    print(f"Сортировка товаров в порядке: {sort_order}...")
    data.sort(key=lambda x: x["name"].lower(), reverse=(sort_order == "desc"))

    # Сохранение данных
    print(f"Сохранение данных в {output_format} формате...")
    if output_format == "csv":
        save_to_csv_and_xlsx(data, f"{output_filename}.csv", None)
    elif output_format == "xlsx":
        save_to_csv_and_xlsx(data, None, f"{output_filename}.xlsx")

    print("Данные успешно сохранены.")

def main():
    parser = argparse.ArgumentParser(description="Парсеры M.Video и DNS.")
    parser.add_argument(
        "parser", choices=["mvideo", "dns"],
        help="Выберите парсер: 'mvideo' или 'dns'."
    )
    parser.add_argument(
        "-f", "--format", choices=["csv", "xlsx"], required=True,
        help="Формат сохранения данных (csv или xlsx)."
    )
    parser.add_argument(
        "-o", "--output", type=str, default="products",
        help="Имя файла для сохранения данных (без расширения)."
    )
    parser.add_argument(
        "-s", "--sort", choices=["asc", "desc"], default="asc",
        help="Порядок сортировки товаров: asc (по возрастанию) или desc (по убыванию)."
    )

    args = parser.parse_args()

    if args.parser == "mvideo":
        run_mvideo_parser(args.format, args.output, args.sort)
    elif args.parser == "dns":
        run_dns_parser(args.format, args.output, args.sort)

if __name__ == "__main__":
    main()
