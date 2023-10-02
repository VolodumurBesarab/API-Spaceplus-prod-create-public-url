import builtins


class LogCreator:

    def __init__(self):
        self.log_file = open('log.txt', 'a')

    def custom_print(self, *args, **kwargs):
        # Конвертуємо всі аргументи у рядок та об'єднуємо їх
        log_message = ' '.join(map(str, args))

        # Записуємо вивід у файл log.txt
        self.log_file.write(log_message)
        self.log_file.write('\n')