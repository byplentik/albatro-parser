import csv
from openpyxl import Workbook

def save_to_csv_and_xls(data, csv_filename=None, xls_filename=None):
    """
    Сохраняет данные в файлы форматов CSV и XLS (если указаны соответствующие параметры).

    :param data: Список словарей, где каждый словарь — это строка данных.
    :param csv_filename: Имя файла для сохранения в формате CSV (или None).
    :param xls_filename: Имя файла для сохранения в формате XLS (или None).
    """
    if csv_filename:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = data[0].keys() if data else []
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    if xls_filename:
        workbook = Workbook()
        sheet = workbook.active

        if data:
            # Записываем заголовки
            headers = list(data[0].keys())
            sheet.append(headers)

            # Записываем строки данных
            for row in data:
                sheet.append([row[key] for key in headers])

        workbook.save(xls_filename)