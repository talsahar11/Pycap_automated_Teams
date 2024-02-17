import string
from time import sleep


class JsonKeysGrabber:
    def __init__(self, input_file):
        self.input_file = input_file
        self.isRunning = False

    def stop(self):
        self.isRunning = False

    def start(self):
        self.isRunning = True
        with open(self.input_file, 'r') as file:
            while self.isRunning:
                where = file.tell()
                line = file.readline()
                if not line:
                    sleep(1)
                    file.seek(where)
                else:
                    if isKeyLine(line):
                        print(extractKey(line))


def isKeyLine(line):
    return "json.key" in line


def extractKey(line: string):
    value_start_index = line.find('"', line.find('"',line.find('"') + 1) + 1) + 1
    value_end_index = len(line) - 2
    return line[value_start_index:value_end_index]