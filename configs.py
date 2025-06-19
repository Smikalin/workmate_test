import argparse


def configure_argument_parser() -> argparse.ArgumentParser:
    """Настройка парсера аргументов."""
    parser = argparse.ArgumentParser(
        description='CSV файл с фильтрацией и агрегацией'
    )
    parser.add_argument('--file', required=True, help='Path to CSV file')
    parser.add_argument(
        '--where',
        help='Фильтрация в формате "column=value" или "column>value"',
    )
    parser.add_argument(
        '--order-by',
        help='Сортировка в формате "column=asc" или "column=desc"',
    )
    parser.add_argument(
        '--aggregate',
        help='Агрегация в формате "column=operation"',
    )
    return parser
