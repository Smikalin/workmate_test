class DataError(Exception):
    """Ошибка данных."""


class DataFilterError(DataError):
    """Ошибка фильтрации данных."""


class DataAggregateError(DataError):
    """Ошибка агрегации данных."""


class IsNumericColumnError(DataError):
    """Ошибка проверки числовых значений."""
