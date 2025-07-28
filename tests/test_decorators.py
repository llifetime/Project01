import os
import pytest
from src.decorators import log  # Замените `your_module` на имя вашего модуля


# Вспомогательная функция для чтения файла логов (если он есть)
def read_log_file(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Тест на логирование в консоль (без filename)
def test_log_to_console(capsys):
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert "add - начато выполнение" in captured.out
    assert "add - успешно завершено. Результат: 5" in captured.out

# Тест на логирование ошибки в консоль
def test_log_error_to_console(capsys):
    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide - начато выполнение" in captured.out
    assert "divide - ошибка: ZeroDivisionError" in captured.out
    assert "Аргументы: 10, 0" in captured.out

# Тест на логирование в файл
def test_log_to_file(tmp_path):
    log_file = tmp_path / "test.log"

    @log(filename=log_file)
    def multiply(a, b):
        return a * b

    result = multiply(3, 4)

    log_content = read_log_file(log_file)
    assert result == 12
    assert "multiply - начато выполнение" in log_content
    assert "multiply - успешно завершено. Результат: 12" in log_content

# Тест на логирование ошибки в файл
def test_log_error_to_file(tmp_path):
    log_file = tmp_path / "error.log"

    @log(filename=log_file)
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    log_content = read_log_file(log_file)
    assert "divide - начато выполнение" in log_content
    assert "divide - ошибка: ZeroDivisionError" in log_content
    assert "Аргументы: 10, 0" in log_content

# Тест на сохранение метаданных функции
def test_log_preserves_function_metadata():
    @log()
    def example_func(a: int, b: int) -> int:
        """Пример функции с документацией."""
        return a + b

    assert example_func.__name__ == "example_func"
    assert example_func.__doc__ == "Пример функции с документацией."
    assert example_func.__annotations__ == {"a": int, "b": int, "return": int}