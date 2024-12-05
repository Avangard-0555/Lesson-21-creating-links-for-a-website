import re
import numpy as np


class NumberAnalyzer:
    def __init__(self):
        pass

    def extract_numbers(self, text):
        """Извлекает числа из текста."""
        pattern = r'\d+(\.\d+)?|\d+\,\d+'
        matches = re.findall(pattern, text)
        numbers = [float(match.replace(',', '.')) for match in matches]
        return numbers

    def arithmetic_operations(self, numbers, operation):
        """Выполняет арифметическую операцию над числами."""
        if not numbers:
            return "Введите числа для выполнения операции."

        if operation == 'sum':
            result = sum(numbers)
        elif operation == 'product':
            result = np.prod(numbers)
        elif operation == 'average':
            result = np.mean(numbers)
        elif operation == 'median':
            result = np.median(numbers)
        elif operation == 'mode':
            result = np.bincount(numbers).argmax()
        elif operation == 'std_dev':
            result = np.std(numbers)
        else:
            return "Неподдерживаемая операция."

        return f"Результат операции '{operation}': {result:.2f}"

    def sort_numbers(self, numbers, order='asc'):
        """Сортирует список чисел."""
        if not numbers:
            return "Нет чисел для сортировки."

        sorted_numbers = sorted(numbers)
        if order == 'desc':
            sorted_numbers.reverse()

        return f"Сортированные числа ({order}): {sorted_numbers}"

    def convert_to_binary(self, number):
        """Конвертирует целое число в двоичное представление."""
        try:
            binary_representation = bin(int(number))[2:]
            return f"Двоичная форма числа {number}: {binary_representation}"
        except ValueError:
            return "Ошибка: неверно указанное число."