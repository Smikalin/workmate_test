from typing import Any, Dict, List


def get_aggregate_data(
    data: List[Dict[str, Any]],
    column: str,
) -> Dict[str, float]:
    """Получает данные для агрегации."""
    return {
        'avg': sum(float(row[column]) for row in data) / len(data),
        'min': min(float(row[column]) for row in data),
        'max': max(float(row[column]) for row in data),
    }


def get_filter_data(
    data: List[Dict[str, Any]],
    column: str,
    value: str,
) -> Dict[str, List[Dict[str, Any]]]:
    """Получает отфильтрованные данные."""
    return {
        '=': [row for row in data if str(row[column]) == value],
        '>': [
            row
            for row in data
            if is_numeric_column(data, column)
            and float(row[column]) > float(value)
        ],
        '<': [
            row
            for row in data
            if is_numeric_column(data, column)
            and float(row[column]) < float(value)
        ],
    }


def get_key(row: Dict[str, Any], column: str) -> Any:
    """Получает ключ для сортировки."""
    try:
        return float(row[column])
    except (ValueError, TypeError):
        return str(row[column])


def is_numeric_column(data: List[Dict[str, Any]], column: str) -> bool:
    """Проверяет, содержит ли столбец только числовые значения."""
    try:
        for row in data:
            float(row[column])
        return True
    except (ValueError, TypeError):
        return False
