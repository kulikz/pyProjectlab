#!/usr/bin/env python3
"""
Лабораторная работа №16
Извлечение данных из лог-файла с помощью регулярных выражений
"""

import re


def read_log_file(filename: str) -> list:
    """
    Читает файл и возвращает список строк

    Args:
        filename: имя файла

    Returns:
        список строк файла
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден!")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def extract_ip_addresses(log_lines: list) -> list:
    """
    Извлекает IP-адреса из строк лога

    Шаблон: ###.###.###.### где # - цифра от 0 до 9
    Учитываются IPv4 адреса от 0.0.0.0 до 255.255.255.255

    Args:
        log_lines: список строк лога

    Returns:
        список найденных IP-адресов
    """
    pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    all_ips = []

    for line in log_lines:
        ips = re.findall(pattern, line)
        all_ips.extend(ips)

    return all_ips


def extract_error_codes(log_lines: list) -> list:
    """
    Извлекает коды ошибок (HTTP status codes) из строк лога

    Коды ошибок находятся после кавычек и состоят из 3 цифр

    Args:
        log_lines: список строк лога

    Returns:
        список найденных кодов ошибок
    """
    # Ищем 3-значные числа после "] \"...\" " (пробел после кавычек)
    pattern = r'"(?:GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)[^"]*"\s+(\d{3})'
    all_codes = []

    for line in log_lines:
        codes = re.findall(pattern, line)
        all_codes.extend(codes)

    return all_codes


def extract_methods_and_urls(log_lines: list) -> list:
    """
    Извлекает HTTP метод и URL из строк лога

    Формат: "МЕТОД URL"

    Args:
        log_lines: список строк лога

    Returns:
        список кортежей (метод, URL)
    """
    pattern = r'"(\w+)\s+([^\s"]+)\s+HTTP/\d+\.\d+"'
    results = []

    for line in log_lines:
        matches = re.findall(pattern, line)
        for match in matches:
            method, url = match
            results.append((method, url))

    return results


def parse_log_line(line: str) -> dict:
    """
    Полностью разбирает одну строку лога с помощью одного регулярного выражения

    Args:
        line: строка лога

    Returns:
        словарь с извлеченными данными
    """
    pattern = re.compile(
        r'^(?P<ip>(?:\d{1,3}\.){3}\d{1,3})\s+'
        r'-\s+-\s+'
        r'\[[^\]]+\]\s+'
        r'"(?P<method>\w+)\s+'
        r'(?P<url>[^\s"]+)\s+'
        r'HTTP/\d+\.\d+"\s+'
        r'(?P<status>\d{3})\s+'
        r'(?P<size>\d+)$'
    )

    match = pattern.match(line.strip())
    if match:
        return match.groupdict()
    return {}


def display_results(ip_list: list, code_list: list, method_url_list: list) -> None:
    """
    Выводит результаты извлечения данных

    Args:
        ip_list: список IP-адресов
        code_list: список кодов ошибок
        method_url_list: список (метод, URL)
    """
    print("=" * 60)
    # Вывод IP-адресов
    print("\n1. НАЙДЕННЫЕ IP-АДРЕСА:")
    print("-" * 40)
    if ip_list:
        for i, ip in enumerate(ip_list, 1):
            print(f"   {i}. {ip}")
        print(f"\n   Всего найдено: {len(ip_list)}")
    else:
        print("   IP-адреса не найдены")

    # Вывод кодов ошибок
    print("\n2. НАЙДЕННЫЕ КОДЫ ОШИБОК (HTTP status codes):")
    print("-" * 40)
    if code_list:
        for i, code in enumerate(code_list, 1):
            status_codes = {
                '200': 'OK',
                '401': 'Unauthorized',
                '403': 'Forbidden',
                '404': 'Not Found',
                '500': 'Internal Server Error'
            }
            description = status_codes.get(code, 'Неизвестный код')
            print(f"   {i}. {code} ({description})")
        print(f"\n   Всего найдено: {len(code_list)}")
    else:
        print("   Коды ошибок не найдены")

    # Вывод методов и URL
    print("\n3. НАЙДЕННЫЕ МЕТОДЫ И URL:")
    print("-" * 40)
    if method_url_list:
        for i, (method, url) in enumerate(method_url_list, 1):
            print(f"   {i}. [{method}] {url}")
        print(f"\n   Всего найдено: {len(method_url_list)}")
    else:
        print("   Методы и URL не найдены")

    # Статистика
    print("\n" + "=" * 60)
    print("СТАТИСТИКА:")
    print("-" * 40)

    if code_list:
        from collections import Counter
        code_counter = Counter(code_list)
        print("   Распределение кодов ошибок:")
        for code, count in sorted(code_counter.items()):
            print(f"     - {code}: {count} раз(а)")

    if method_url_list:
        method_counter = Counter(method for method, _ in method_url_list)
        print("\n   Распределение HTTP методов:")
        for method, count in sorted(method_counter.items()):
            print(f"     - {method}: {count} раз(а)")


def main():
    """Основная функция программы"""
    # Имя входного файла
    input_file = "input.txt"

    # Чтение файла
    print("Чтение файла input.txt...")
    log_lines = read_log_file(input_file)

    if not log_lines:
        print("Нет данных для обработки.")
        return

    print(f"Файл прочитан. Количество строк: {len(log_lines)}")

    # Извлечение данных
    print("\nОбработка данных с помощью регулярных выражений...")

    # Способ 1: отдельные функции для каждого типа данных
    ip_list = extract_ip_addresses(log_lines)
    code_list = extract_error_codes(log_lines)
    method_url_list = extract_methods_and_urls(log_lines)

    # Вывод результатов
    display_results(ip_list, code_list, method_url_list)

    # Способ 2: полный разбор строк (более детально)
    print("\n" + "=" * 60)
    print("ДЕТАЛЬНЫЙ РАЗБОР КАЖДОЙ СТРОКИ:")
    print("=" * 60)

    for i, line in enumerate(log_lines, 1):
        parsed = parse_log_line(line)
        if parsed:
            print(f"\nСтрока {i}:")
            print(f"  IP-адрес: {parsed.get('ip', '-')}")
            print(f"  Метод: {parsed.get('method', '-')}")
            print(f"  URL: {parsed.get('url', '-')}")
            print(f"  Код: {parsed.get('status', '-')}")
            print(f"  Размер: {parsed.get('size', '-')}")


if __name__ == "__main__":
    main()