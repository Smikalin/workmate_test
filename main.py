import csv
from typing import Any, Dict, List

from tabulate import tabulate

from configs import configure_argument_parser
from constants import FILTER_OPERATORS
from exceptions import (
    DataAggregateError,
    DataError,
    DataFilterError,
    IsNumericColumnError,
)
from utils import (
    get_aggregate_data,
    get_filter_data,
    get_key,
    is_numeric_column,
)


def read_csv(file_path: str) -> List[Dict[str, Any]]:
    """Читает CSV файл и возвращает список словарей."""
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def filter_data(
    data: List[Dict[str, Any]],
    condition: str,
) -> List[Dict[str, Any]]:
    """Фильтрует данные по числовым значениям в соответствии с условием."""
    for operator in FILTER_OPERATORS:
        if operator in condition:
            column, value = condition.split(operator)
            value = value.strip('"')
            return get_filter_data(data, column, value)[operator]
    raise DataFilterError(
        f"Неподдерживаемый оператор. "
        f"Используйте: {', '.join(FILTER_OPERATORS)}"
    )


def sort_data(
    data: List[Dict[str, Any]],
    condition: str,
) -> List[Dict[str, Any]]:
    """Сортирует данные в соответствии с условием."""
    column, order = condition.split("=")
    return sorted(
        data,
        key=lambda row: get_key(row, column),
        reverse=(order == "desc"),
    )


def aggregate_data(
    data: List[Dict[str, Any]],
    condition: str,
) -> List[Dict[str, Any]]:
    """Вычисляет агрегацию на основе условия."""
    column, operation = condition.split("=")

    if not data:
        raise DataError("Данные пусты")

    if not is_numeric_column(data, column):
        raise IsNumericColumnError(f"Столбец '{column}' не является числовым")

    result = get_aggregate_data(data, column)

    if operation not in result.keys():
        raise DataAggregateError(
            f"Неподдерживаемая операция '{operation}'. "
            f"Используйте: {', '.join(result.keys())}"
        )

    return [{f"{operation}": f"{result[operation]:.2f}"}]


def main():
    try:
        parser = configure_argument_parser()
        args = parser.parse_args()

        if not args.file:
            raise DataError("Не указан файл")

        data = read_csv(args.file)

        if args.where:
            data = filter_data(data, args.where)

        if args.order_by:
            data = sort_data(data, args.order_by)

        if args.aggregate:
            data = aggregate_data(data, args.aggregate)

        print(tabulate(data, headers="keys", tablefmt="grid"))

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
