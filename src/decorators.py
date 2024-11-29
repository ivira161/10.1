def log(filename=None):
    '''Декоратор log, который автоматически записывает логи функции, а также ее результаты или возникшие ошибки.'''

    def decorator(func):
        def wrapper(*args, **kwargs):
            log_message = f"Starting '{func.__name__}' with args: {args} and kwargs: {kwargs}\n"
            if filename:
                with open(filename, 'a') as f:
                    f.write(log_message)
            else:
                print(log_message, end='')

            try:
                result = func(*args, **kwargs)
                log_message = f"'{func.__name__}' ok, result: {result}\n"
            except Exception as e:
                log_message = f"'{func.__name__}' error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')
                raise

            if filename:
                with open(filename, 'a') as f:
                    f.write(log_message)
            else:
                print(log_message, end='')

            return result

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


my_function(1, 2)  # Успешное выполнение функции


@log()
def my_function_with_error(x, y):
    return x / y
