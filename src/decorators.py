import functools
from datetime import datetime


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Формируем строку с информацией о начале выполнения функции
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message_start = f"{start_time} - {func.__name__} - начато выполнение\n"

            # Логируем входные параметры (если нужно)
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            log_message_args = f"Аргументы: {signature}\n" if (args or kwargs) else ""

            try:
                # Выводим логи в консоль или файл (начало)
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message_start + log_message_args)
                else:
                    print(log_message_start + log_message_args, end='')

                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем строку с результатом
                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_message_success = f"{end_time} - {func.__name__} - успешно завершено. Результат: {result}\n"

                # Логируем успешное завершение
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message_success)
                else:
                    print(log_message_success, end='')

                return result

            except Exception as e:
                # Формируем строку с ошибкой
                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_message_error = f"{end_time} - {func.__name__} - ошибка: {type(e).__name__}: {e}. Аргументы: {signature}\n"

                # Логируем ошибку
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message_error)
                else:
                    print(log_message_error, end='')
                raise  # Пробрасываем исключение дальше

        return wrapper

    return decorator