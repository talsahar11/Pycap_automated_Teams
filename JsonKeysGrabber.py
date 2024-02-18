import logging
import select
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
        foundPairs = list()
        current_val = None
        with open(self.input_file, 'r') as file:
            while self.isRunning:
                read_ready, write_ready, error_ready = select.select([file], [], [])
                line = file.readline()
                if file in read_ready:
                    if isValueLine(line):
                        current_val = extractKey(line)
                    elif isKeyLine(line):
                        if current_val is None:
                            logging.error(f"key without a michse: {extractKey(line)}")
                        else:
                            foundPairs.append((extractKey(line), current_val))
                            print(foundPairs.pop(len(foundPairs) - 1))
                            current_val = None


def isKeyLine(line):
    return "json.key" in line


def isValueLine(line):
    return "json.value" in line


def extractKey(line: string):
    value_start_index = line.find('"', line.find('"',line.find('"') + 1) + 1) + 1
    value_end_index = len(line) - 2
    return line[value_start_index:value_end_index]
