import functools


def log(filename=None):
    """Декоратор для логирования выполнения функций.

    Логирует успешное выполнение или ошибки функции в указанный файл или консоль.
    Формат логов:
    - При успехе: "{function_name} ok"
    - При ошибке: "{function_name} error: {error_type}. Inputs: ({args}, {kwargs})"

    Args:
        filename (str, optional): Имя файла для записи логов. Если не указан,
                                  логи выводятся в консоль.

    Returns:
        function: Декорированная функция с логированием.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем строку успешного выполнения
                log_message = f"{func.__name__} ok\n"

                # Логируем
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')

                return result

            except Exception as e:
                # Формируем строку с ошибкой
                args_repr = [repr(a) for a in args]
                kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)

                log_message = f"{func.__name__} error: {type(e).__name__}. Inputs: ({signature})\n"

                # Логируем ошибку
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')
                raise  # Пробрасываем исключение дальше

        return wrapper

    return decorator