import pytest
import tempfile
import os
from unittest.mock import patch

from main import read_csv, filter_data, sort_data, aggregate_data, main
from utils import is_numeric_column, get_key, get_filter_data, get_aggregate_data


@pytest.fixture
def sample_csv_data():
    """Образец данных CSV для тестирования."""
    return [
        {
            'name': 'iphone 15 pro',
            'brand': 'apple',
            'price': '999',
            'rating': '4.9',
        },
        {
            'name': 'galaxy s23 ultra',
            'brand': 'samsung',
            'price': '1199',
            'rating': '4.8',
        },
        {
            'name': 'redmi note 12',
            'brand': 'xiaomi',
            'price': '199',
            'rating': '4.6',
        },
        {
            'name': 'poco x5 pro',
            'brand': 'xiaomi',
            'price': '299',
            'rating': '4.4',
        },
    ]


@pytest.fixture
def sample_csv_file(sample_csv_data):
    """Создает временный CSV файл для тестирования."""
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.csv',
        delete=False,
    ) as f:
        f.write('name,brand,price,rating\n')
        for row in sample_csv_data:
            f.write(
                f'{row["name"]},'
                f'{row["brand"]},'
                f'{row["price"]},'
                f'{row["rating"]}\n'
            )
        temp_file = f.name

    yield temp_file
    os.unlink(temp_file)


class TestReadCSV:
    """Тесты для функции read_csv."""

    def test_read_csv_success(self, sample_csv_file):
        """Тест на успешное чтение CSV файла."""
        result = read_csv(sample_csv_file)
        assert len(result) == 4
        assert result[0]['name'] == 'iphone 15 pro'
        assert result[0]['brand'] == 'apple'
        assert result[0]['price'] == '999'
        assert result[0]['rating'] == '4.9'

    def test_read_csv_file_not_found(self):
        """Тест на чтение несуществующего файла."""
        with pytest.raises(FileNotFoundError):
            read_csv('nonexistent.csv')


class TestFilterData:
    """Тесты для функции filter_data."""

    def test_filter_equals_text(self, sample_csv_data):
        """Тест на фильтрацию с оператором равенства на текстовом столбце."""
        result = filter_data(sample_csv_data, 'brand=apple')
        assert len(result) == 1
        assert result[0]['brand'] == 'apple'

    def test_filter_equals_numeric(self, sample_csv_data):
        """Тест на фильтрацию с оператором равенства на числовом столбце."""
        result = filter_data(sample_csv_data, 'price=999')
        assert len(result) == 1
        assert result[0]['price'] == '999'

    def test_filter_greater_than(self, sample_csv_data):
        """Тест на фильтрацию с оператором больше."""
        result = filter_data(sample_csv_data, 'price>500')
        assert len(result) == 2
        assert all(float(row["price"]) > 500 for row in result)

    def test_filter_less_than(self, sample_csv_data):
        """Тест на фильтрацию с оператором меньше."""
        result = filter_data(sample_csv_data, 'price<500')
        assert len(result) == 2
        assert all(float(row["price"]) < 500 for row in result)

    def test_filter_no_matches(self, sample_csv_data):
        """Тест на фильтрацию без совпадений."""
        result = filter_data(sample_csv_data, 'brand=sony')
        assert len(result) == 0

    def test_filter_invalid_operator(self, sample_csv_data):
        """Тест на фильтрацию с неверным оператором."""
        with pytest.raises(Exception):
            filter_data(sample_csv_data, 'price>=500')

    def test_filter_with_quotes(self, sample_csv_data):
        """Тест на фильтрацию с кавычками."""
        result = filter_data(sample_csv_data, 'brand="apple"')
        assert len(result) == 1
        assert result[0]['brand'] == 'apple'


class TestSortData:
    """Тесты для функции sort_data."""

    def test_sort_ascending_numeric(self, sample_csv_data):
        """Тест на сортировку числового столбца по возрастанию."""
        result = sort_data(sample_csv_data, 'price=asc')
        prices = [float(row['price']) for row in result]
        assert prices == sorted(prices)

    def test_sort_descending_numeric(self, sample_csv_data):
        """Тест на сортировку числового столбца по убыванию."""
        result = sort_data(sample_csv_data, 'price=desc')
        prices = [float(row['price']) for row in result]
        assert prices == sorted(prices, reverse=True)

    def test_sort_ascending_text(self, sample_csv_data):
        """Тест на сортировку текстового столбца по возрастанию."""
        result = sort_data(sample_csv_data, 'brand=asc')
        brands = [row['brand'] for row in result]
        assert brands == sorted(brands)

    def test_sort_descending_text(self, sample_csv_data):
        """Тест на сортировку текстового столбца по убыванию."""
        result = sort_data(sample_csv_data, 'brand=desc')
        brands = [row['brand'] for row in result]
        assert brands == sorted(brands, reverse=True)


class TestAggregateData:
    """Тесты для функции aggregate_data."""

    def test_aggregate_avg(self, sample_csv_data):
        """Тест на агрегацию среднего значения."""
        result = aggregate_data(sample_csv_data, 'price=avg')
        assert len(result) == 1
        assert 'avg' in result[0]
        expected_avg = (999 + 1199 + 199 + 299) / 4
        assert abs(float(result[0]['avg']) - expected_avg) < 0.01

    def test_aggregate_min(self, sample_csv_data):
        """Тест на агрегацию минимального значения."""
        result = aggregate_data(sample_csv_data, 'price=min')
        assert len(result) == 1
        assert 'min' in result[0]
        assert float(result[0]['min']) == 199.0

    def test_aggregate_max(self, sample_csv_data):
        """Тест на агрегацию максимального значения."""
        result = aggregate_data(sample_csv_data, 'price=max')
        assert len(result) == 1
        assert 'max' in result[0]
        assert float(result[0]['max']) == 1199.0

    def test_aggregate_empty_data(self):
        """Тест на агрегацию с пустыми данными."""
        with pytest.raises(Exception):
            aggregate_data([], 'price=avg')

    def test_aggregate_non_numeric_column(self, sample_csv_data):
        """Тест на агрегацию на нечисловом столбце."""
        with pytest.raises(Exception):
            aggregate_data(sample_csv_data, 'brand=avg')

    def test_aggregate_invalid_operation(self, sample_csv_data):
        """Тест на агрегацию с неверной операцией."""
        with pytest.raises(Exception):
            aggregate_data(sample_csv_data, 'price=sum')


class TestUtils:
    """Тесты для функций модуля utils."""

    def test_is_numeric_column_true(self, sample_csv_data):
        """Тест на обнаружение числового столбца."""
        assert is_numeric_column(sample_csv_data, 'price') is True

    def test_is_numeric_column_false(self, sample_csv_data):
        """Тест на обнаружение текстового столбца."""
        assert is_numeric_column(sample_csv_data, 'brand') is False

    def test_get_key_numeric(self, sample_csv_data):
        """Тест на получение ключа для числового значения."""
        key = get_key(sample_csv_data[0], 'price')
        assert key == 999.0

    def test_get_key_text(self, sample_csv_data):
        """Тест на получение ключа для текстового значения."""
        key = get_key(sample_csv_data[0], 'brand')
        assert key == 'apple'

    def test_get_filter_data_equals(self, sample_csv_data):
        """Тест на получение отфильтрованных данных для оператора равенства."""
        result = get_filter_data(sample_csv_data, 'brand', 'apple')
        assert len(result['=']) == 1
        assert result['='][0]['brand'] == 'apple'

    def test_get_filter_data_greater_than(self, sample_csv_data):
        """Тест на получение отфильтрованных данных для оператора больше."""
        result = get_filter_data(sample_csv_data, 'price', '500')
        assert len(result['>']) == 2

    def test_get_filter_data_less_than(self, sample_csv_data):
        """Тест на получение отфильтрованных данных для оператора меньше."""
        result = get_filter_data(sample_csv_data, 'price', '500')
        assert len(result['<']) == 2

    def test_get_aggregate_data(self, sample_csv_data):
        """Тест на получение данных для агрегации."""
        result = get_aggregate_data(sample_csv_data, 'price')
        assert 'avg' in result
        assert 'min' in result
        assert 'max' in result
        assert result['min'] == 199.0
        assert result['max'] == 1199.0


class TestIntegration:
    """Тесты для интеграции."""

    def test_filter_and_sort(self, sample_csv_data):
        """Тест на фильтрацию и сортировку."""
        filtered = filter_data(sample_csv_data, 'price>500')
        sorted_data = sort_data(filtered, 'price=desc')
        prices = [float(row['price']) for row in sorted_data]
        assert prices == sorted(prices, reverse=True)

    def test_filter_and_aggregate(self, sample_csv_data):
        """Тест на фильтрацию и агрегацию."""
        filtered = filter_data(sample_csv_data, 'price>500')
        result = aggregate_data(filtered, 'price=avg')
        assert len(result) == 1
        assert 'avg' in result[0]

    def test_sort_and_aggregate(self, sample_csv_data):
        """Тест на сортировку и агрегацию."""
        sorted_data = sort_data(sample_csv_data, 'price=desc')
        result = aggregate_data(sorted_data, 'price=max')
        assert len(result) == 1
        assert float(result[0]['max']) == 1199.0


class TestMain:
    """Тесты для функции main."""

    @patch('main.configure_argument_parser')
    @patch('main.read_csv')
    @patch('main.tabulate')
    def test_main_file_only(self, mock_tabulate, mock_read_csv, mock_parser):
        """Тест на выполнение функции main с только файлом."""
        mock_args = type(
            'Args',
            (),
            {
                'file': 'test.csv',
                'where': None,
                'order_by': None,
                'aggregate': None,
            },
        )()
        mock_parser.return_value.parse_args.return_value = mock_args

        mock_data = [{'test': 'data'}]
        mock_read_csv.return_value = mock_data

        mock_tabulate.return_value = 'table'

        with patch('builtins.print') as mock_print:
            main()

        mock_read_csv.assert_called_once_with('test.csv')
        mock_tabulate.assert_called_once_with(
            mock_data, headers='keys', tablefmt='grid'
        )
        mock_print.assert_called_once_with('table')

    @patch('main.configure_argument_parser')
    @patch('main.read_csv')
    @patch('main.filter_data')
    @patch('main.tabulate')
    def test_main_with_filter(
        self, mock_tabulate, mock_filter, mock_read_csv, mock_parser
    ):
        """Тест на выполнение функции main с фильтрацией."""
        mock_args = type(
            'Args',
            (),
            {
                'file': 'test.csv',
                'where': 'price>500',
                'order_by': None,
                'aggregate': None,
            },
        )()
        mock_parser.return_value.parse_args.return_value = mock_args

        mock_data = [{'test': 'data'}]
        mock_filtered_data = [{'filtered': 'data'}]
        mock_read_csv.return_value = mock_data
        mock_filter.return_value = mock_filtered_data

        mock_tabulate.return_value = 'table'

        with patch('builtins.print'):
            main()

        mock_filter.assert_called_once_with(mock_data, 'price>500')
        mock_tabulate.assert_called_once_with(
            mock_filtered_data, headers='keys', tablefmt='grid'
        )

    @patch('main.configure_argument_parser')
    @patch('main.read_csv')
    @patch('main.sort_data')
    @patch('main.tabulate')
    def test_main_with_sort(self, mock_tabulate, mock_sort, mock_read_csv, mock_parser):
        """Тест на выполнение функции main с сортировкой."""
        mock_args = type(
            'Args',
            (),
            {
                'file': 'test.csv',
                'where': None,
                'order_by': 'price=desc',
                'aggregate': None,
            },
        )()
        mock_parser.return_value.parse_args.return_value = mock_args

        mock_data = [{'test': 'data'}]
        mock_sorted_data = [{'sorted': 'data'}]
        mock_read_csv.return_value = mock_data
        mock_sort.return_value = mock_sorted_data

        mock_tabulate.return_value = 'table'

        with patch('builtins.print'):
            main()

        mock_sort.assert_called_once_with(mock_data, 'price=desc')
        mock_tabulate.assert_called_once_with(
            mock_sorted_data, headers='keys', tablefmt='grid'
        )

    @patch('main.configure_argument_parser')
    @patch('main.read_csv')
    @patch('main.aggregate_data')
    @patch('main.tabulate')
    def test_main_with_aggregate(
        self, mock_tabulate, mock_aggregate, mock_read_csv, mock_parser
    ):
        """Тест на выполнение функции main с агрегацией."""
        mock_args = type(
            'Args',
            (),
            {
                'file': 'test.csv',
                'where': None,
                'order_by': None,
                'aggregate': 'price=avg',
            },
        )()
        mock_parser.return_value.parse_args.return_value = mock_args

        mock_data = [{'test': 'data'}]
        mock_agg_data = [{'avg': '100.00'}]
        mock_read_csv.return_value = mock_data
        mock_aggregate.return_value = mock_agg_data

        mock_tabulate.return_value = 'table'

        with patch('builtins.print'):
            main()

        mock_aggregate.assert_called_once_with(mock_data, 'price=avg')
        mock_tabulate.assert_called_once_with(
            mock_agg_data, headers='keys', tablefmt='grid'
        )

    @patch('main.configure_argument_parser')
    def test_main_no_file(self, mock_parser):
        """Тест на выполнение функции main без файла."""
        mock_args = type(
            'Args',
            (),
            {'file': None, 'where': None, 'order_by': None, 'aggregate': None},
        )()
        mock_parser.return_value.parse_args.return_value = mock_args

        with patch('builtins.print') as mock_print:
            main()

        mock_print.assert_called_once_with('Ошибка: Не указан файл')


if __name__ == '__main__':
    pytest.main(
        [
            __file__,
            '-v',
            '--cov=main',
            '--cov=configs',
            '--cov-report=term-missing',
        ]
    )
