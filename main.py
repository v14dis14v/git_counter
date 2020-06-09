import os
import re
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
import MuteException

# Контейнер для сбора статистики пользователя
user_stats = {}

# "Константа" для поиска пустых репозиториев
EMPTY_PROJECT = "does not have any commits yet"

# Конфигурация логера
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "git_counter.log"

"""
Сбор Console Handler

@return StreamHandler
"""
def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)

   return console_handler

"""
Сборка file handler

@return TimedRotatingFileHandler
"""
def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)

   return file_handler

"""
Сборка логера

@param string logger_name Имя логера

@return logger
"""
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG)
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())

   logger.propagate = False

   return logger

log = get_logger('git_counter')

"""
Подсчёт количества закомиченных строк

@param string name Имя пользователя в git

@return int
"""
def get_count_lines(name):
    try:
        project_stats = os.popen("git log --pretty=format:==%an --numstat").read()
    except MuteException:
        return 0

    matches     = re.finditer('(==(.+))\n(([\d,-]+)\t([\d,-]+)\t(.+)\n)*', project_stats, re.MULTILINE)
    lines_added = 0

    for _, match in enumerate(matches, start=1):
        if match.group(2) != name:
            continue
        
        current_lines_added = match.group(4)

        if current_lines_added == None or current_lines_added == '-':
            continue

        current_lines_added = int(current_lines_added)
        file_path           = match.group(6)
        lines_added        += current_lines_added
        
        add_user_stats(file_path, current_lines_added)
    return lines_added

"""
Обновление статистики по файлам

@params string file_path Путь до файла
@params string current_lines_added Количество строк закомиченных в файл

@return void
"""
def add_user_stats(file_path, current_lines_added):
    extension = 'other'

    if '.' in file_path:
        file_extension = re.search(r'(\.(\w+))', file_path)
        extension      = file_extension.group(2)

    if extension in user_stats:
        user_stats[extension] += current_lines_added
    else:
        user_stats[extension] = current_lines_added

"""
Точка входа 

@return void
"""
def main():
    lines = 0
    total = 0

    main_path = input('Enter your main path: ')
    if os.path.exists(main_path)  == False:
        print('Error: path does\'t exist')

    os.chdir(main_path)
    git_user_name = input('Enter your git name: ')
    paths = os.popen('find . -name .git').read().rsplit()

    for current_path in paths:
        os.chdir(f"{main_path}/{current_path}")
        lines += get_count_lines(git_user_name)

    for file_extension, lines_code in user_stats.items():
        print(f"{file_extension} : {lines_code}")
        
    print(f"Всего в строк закомичено: {lines}")

if __name__ == '__main__':
    main()