# CSV Processor

Простой скрипт для обработки CSV-файлов с поддержкой фильтрации, сортировки и агрегации данных.

## Возможности

- **Чтение CSV файлов** - поддержка UTF-8 кодировки
- **Фильтрация данных** - операторы `=`, `>`, `<` для числовых и текстовых колонок
- **Сортировка данных** - по возрастанию (`asc`) и убыванию (`desc`)
- **Агрегация данных** - среднее (`avg`), минимум (`min`), максимум (`max`) для числовых колонок
- **Вывод** - табличное отображение с помощью библиотеки `tabulate`

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Smikalin/workmate_test.git
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/Scripts/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

### Примеры использования

#### 1. Просмотр содержимого файла
```bash
python main.py --file products.csv
```

#### 2. Фильтрация данных
```bash
# Фильтрация по текстовой колонке
python main.py --file products.csv --where "brand=apple"

# Фильтрация по числовой колонке
python main.py --file products.csv --where "price>500"
```

#### 3. Сортировка данных
```bash
# Сортировка по возрастанию
python main.py --file products.csv --order-by "price=asc"

# Сортировка по убыванию
python main.py --file products.csv --order-by "price=desc"

# Сортировка текстовых колонок
python main.py --file products.csv --order-by "brand=asc"
```

#### 4. Агрегация данных
```bash
# Среднее значение
python main.py --file products.csv --aggregate "price=avg"

# Минимальное значение
python main.py --file products.csv --aggregate "price=min"

# Максимальное значение
python main.py --file products.csv --aggregate "price=max"
```

#### 5. Комбинирование операций
```bash
# Фильтрация + сортировка
python main.py --file products.csv --where "price>500" --order-by "price=desc"

# Фильтрация + агрегация
python main.py --file products.csv --where "brand=apple" --aggregate "price=avg"
```

## Тестирование

### Запуск тестов
```bash
# Запуск всех тестов
pytest

# Запуск с отчетом о покрытии
pytest --cov=main --cov=utils --cov=configs --cov-report=term-missing
```

### Покрытие тестами
Текущее покрытие кода тестами составляет **88%**.


## Автор

- [Смикални Никита](https://github.com/Smikalin)
