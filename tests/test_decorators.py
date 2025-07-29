import os
import pytest
import time
from datetime import datetime
from src.decorators import log


class CustomException(Exception):
    pass


def read_log_file(filename):
    """Вспомогательная функция для чтения файла логов"""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def test_log_to_console(capsys):
    """Тест логирования в консоль (успешный случай)"""

    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert "add - начато выполнение" in captured.out
    assert "Аргументы: 2, 3" in captured.out
    assert "add - успешно завершено. Результат: 5" in captured.out


def test_log_error_to_console(capsys):
    """Тест логирования ошибки в консоль"""

    @log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    output = captured.out
    assert "divide - начато выполнение" in output
    assert "Аргументы: 10, 0" in output
    assert "divide - ошибка: ZeroDivisionError" in output


def test_log_to_file(tmp_path):
    """Тест логирования в файл (успешный случай)"""
    log_file = tmp_path / "test.log"

    @log(filename=log_file)
    def greet(name):
        return f"Hello, {name}"

    result = greet("Alice")
    log_content = read_log_file(log_file)

    assert result == "Hello, Alice"
    assert "greet - начато выполнение" in log_content
    assert "Аргументы: 'Alice'" in log_content
    assert "greet - успешно завершено. Результат: Hello, Alice" in log_content


def test_log_error_to_file(tmp_path):
    """Тест логирования ошибки в файл"""
    log_file = tmp_path / "error.log"

    @log(filename=log_file)
    def fail():
        raise ValueError("Invalid value")

    with pytest.raises(ValueError):
        fail()

    log_content = read_log_file(log_file)
    assert "fail - начато выполнение" in log_content
    assert "fail - ошибка: ValueError" in log_content
    assert "Invalid value" in log_content


def test_log_metadata():
    """Тест сохранения метаданных функции"""

    @log()
    def documented_func(a: int) -> str:
        """Тестовая функция"""
        return str(a)

    assert documented_func.__name__ == "documented_func"
    assert documented_func.__doc__ == "Тестовая функция"
    assert documented_func.__annotations__ == {"a": int, "return": str}


def test_log_no_return(capsys):
    """Тест функции без возвращаемого значения"""

    @log()
    def no_return():
        pass

    no_return()
    captured = capsys.readouterr()
    assert "no_return - успешно завершено. Результат: None" in captured.out


def test_log_with_args_kwargs(tmp_path):
    """Тест функции с *args и **kwargs"""
    log_file = tmp_path / "args.log"

    @log(filename=log_file)
    def complex_func(a, *args, **kwargs):
        return f"{a}, {args}, {kwargs}"

    result = complex_func(1, "test", key="value")
    log_content = read_log_file(log_file)

    assert result == "1, ('test',), {'key': 'value'}"
    assert "Аргументы: 1, 'test', key='value'" in log_content


def test_log_custom_exception(capsys):
    """Тест кастомного исключения"""

    @log()
    def raise_custom():
        raise CustomException("Custom error")

    with pytest.raises(CustomException):
        raise_custom()

    captured = capsys.readouterr()
    assert "CustomException" in captured.out
    assert "Custom error" in captured.out


def test_log_multiple_calls(tmp_path):
    """Тест множественных вызовов"""
    log_file = tmp_path / "multi.log"

    @log(filename=log_file)
    def counter():
        return 42

    counter()
    counter()
    log_content = read_log_file(log_file)

    assert log_content.count("counter - начато выполнение") == 2
    assert log_content.count("counter - успешно завершено") == 2


def test_log_special_values(capsys):
    """Тест специальных значений (None, False, 0)"""

    @log()
    def special_values(x):
        return x

    special_values(None)
    special_values(False)
    special_values(0)

    captured = capsys.readouterr()
    assert "Результат: None" in captured.out
    assert "Результат: False" in captured.out
    assert "Результат: 0" in captured.out


def test_log_performance(capsys):
    """Тест производительности с замером времени"""

    @log()
    def slow_func():
        time.sleep(0.1)
        return "done"

    start = time.time()
    slow_func()
    duration = time.time() - start

    captured = capsys.readouterr()
    assert "slow_func" in captured.out
    assert duration >= 0.1