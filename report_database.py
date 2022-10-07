from datetime import datetime
from pathlib import Path


class ReportDatabase:
    def __init__(self, filepath):
        self.__filepath = filepath
        self.__datetime_format = '%Y-%m-%d,%H:%M:%S'
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        with open(filepath, 'r') as file:
            self.__reports = [line.rstrip() for line in file]

    def add(self, app_id):
        report = datetime.now().strftime(self.__datetime_format) + ' ' + app_id
        self.__reports.append(report)

        with open(self.__filepath, 'a') as file:
            file.write(report + '\n')

    def exist(self, app_id):
        for report in self.__reports:
            if report.split(' ')[1] == app_id:
                return True

        return False

    def clear_old(self, lifespan):
        is_modified = False
        for report in self.__reports:
            if (datetime.now() - datetime.strptime(report.split(' ')[0], self.__datetime_format)).days > lifespan:
                self.__reports.remove(report)
                is_modified = True

        if is_modified:
            with open(self.__filepath, 'w') as file:
                for report in self.__reports:
                    file.write(report + '\n')
