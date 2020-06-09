import os
import re

project_stats = {}

"""
Подсчёт количества закомиченных строк

:param string name Имя пользователя в git
:param string app_path путь до приложения

:return array
"""
def get_count_lines(name, app_path):
    project_stats = os.popen(f"bash {app_path}/count.sh").read()
    matches = re.finditer(r'(\w+) (\d+) (\d+)', project_stats, re.MULTILINE)

    for _, match in enumerate(matches, start=1):
        if match.group(1) != name:
            continue

        lines_added = int(match.group(2))
        lines_deleted = int(match.group(3))
        add_user_stats(os.getcwd(), lines_added, lines_deleted)

        return [lines_added, lines_deleted]

    return [0, 0]

"""
Упаковка в словарь 

:param int added число добавленных строк
:param int deleted число удалённых строк
 
:return None
"""
def add_user_stats(file_path, added, deleted):
    project_name = re.search(r'(\w+)\/\.git', file_path).group(1)

    if project_name in project_stats:
        project_stats[project_name]['added'] += added
        project_stats[project_name]['deleted'] += deleted
    else:
        project_stats[project_name] = {'added' : added, 'deleted' : deleted}

"""
Точка входа 

@return void
"""
def main():
    added_lines   = 0
    deleted_lines = 0

    main_path = input('Enter your main path: ')
    if os.path.exists(main_path)  == False:
        print('Error: path does\'t exist')

    app_path = os.path.abspath(__file__)[0: -8]
    os.chdir(main_path)

    name          = os.popen('git config user.name').read().strip()
    git_user_name = input(f'Enter your git name or press Enter to use {name}: ')

    if git_user_name == '':
        git_user_name = name

    paths = os.popen('find . -name .git').read().rsplit()

    for current_path in paths:
        os.chdir(f"{main_path}/{current_path}")
        user_stats = get_count_lines(git_user_name, app_path)
        added_lines   += user_stats[0]
        deleted_lines += user_stats[1]

    for project, lines in project_stats.items():
        print(f"В проекте {project} добавил {lines['added']}, удалил {lines['deleted']}")

    print(f"Всего в строк Закомичено: {added_lines}")
    print(f"Всего в строк Удалено: {deleted_lines}")

if __name__ == '__main__':
    main()