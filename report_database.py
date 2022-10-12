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

    def add(self, item_id_list):
        buffer_report = ''
        for item_id in item_id_list:
            report = datetime.now().strftime(self.__datetime_format) + ' ' + item_id
            self.__reports.append(report)
            buffer_report += report + '\n'
            print(report + ' [added]')

        if buffer_report:
            with open(self.__filepath, 'a') as file:
                file.write(buffer_report)

    def remove(self, item_id_list):
        is_modified = False
        for item_id in item_id_list:
            report = self.find(item_id)
            if report:
                self.__reports.remove(report)
                print(report + ' [removed]')
                is_modified = True

        if is_modified:
            self.__rewrite()

    def remove_old(self, lifespan):
        is_modified = False
        for report in self.__reports.copy():
            if (datetime.now() - datetime.strptime(report.split(' ')[0], self.__datetime_format)).days >= lifespan:
                self.__reports.remove(report)
                print(report + ' [removed]')
                is_modified = True

        if is_modified:
            self.__rewrite()

    def find(self, item_id):
        for report in self.__reports:
            if report.split(' ')[1] == item_id:
                return report

        return ''

    def __rewrite(self):
        buffer_report = ''
        for report in self.__reports:
            buffer_report += report + '\n'

        with open(self.__filepath, 'w') as file:
            file.write(buffer_report)
