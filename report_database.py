from datetime import datetime
from pathlib import Path


class ReportDatabase:
    def __init__(self, filepath):
        self.__reports = {}
        self.__filepath = filepath
        self.__datetime_format = '%Y-%m-%d,%H:%M:%S'
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        with open(filepath, 'r') as file:
            for line in file:
                line_parts = line.rstrip().split(' ')
                self.__reports[line_parts[1]] = line_parts[0]

        print('------' + datetime.now().strftime(self.__datetime_format) + '------')

    def add(self, identifier):
        self.__reports[identifier] = datetime.now().strftime(self.__datetime_format)
        print('(+) ' + identifier)

    def remove(self, identifiers):
        self.__remove(identifiers, self.exist)

    def remove_invalid(self, lifespan):
        self.__remove(self.__reports.copy(), self.is_valid, lifespan)

    def exist(self, identifier):
        return identifier in self.__reports

    def is_valid(self, identifier, lifespan):
        return (datetime.now() - datetime.strptime(self.__reports[identifier], self.__datetime_format)).days >= lifespan

    def save(self):
        buffer_report = ''
        for identifier in self.__reports:
            buffer_report += self.__reports[identifier] + ' ' + identifier + '\n'

        with open(self.__filepath, 'w') as file:
            file.write(buffer_report)

        print('Database synchronized.')

    def __remove(self, identifiers, condition, *con_args):
        for identifier in identifiers:
            if condition(identifier, *con_args):
                self.__reports.pop(identifier)
                print('(-) ' + identifier)
