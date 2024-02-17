import string
from time import sleep


class JsonStripper:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.__isRunning = False

    def run(self):
        self.__isRunning = True
        self.analyze()

    def shutdown(self):
        self.__isRunning = False

    def analyze(self):
        json_started = False
        json_lines = []
        json_indentation = 0
        with open(self.output_file, 'w') as jsonsFile:
            with open(self.input_file, 'r') as file:
                while self.__isRunning:
                    where = file.tell()  # Get current file position
                    line = file.readline()
                    print(f"Nothing stripped: {where}")
                    if not line:
                        sleep(0.1)
                        file.seek(where)
                    else:
                        # Count leading whitespace characters to determine indentation level
                        indentation = len(line) - len(line.lstrip())

                        # Strip whitespace from the beginning and end of the line
                        stripped_line = line.strip()

                        # Check if the line contains '"json": {'
                        if stripped_line == '"json": {':
                            print("FOund shitty json")
                            json_started = True
                            json_lines.append(line)
                            json_indentation = indentation
                            continue  # Skip to the next line

                        # If JSON parsing has started, append the line to json_lines
                        if json_started:
                            json_lines.append(line)
                            print("FOund shitty json")

                            # Check if the line contains a closing '}'
                            if stripped_line == '}' or stripped_line == '},':
                                # Check if the indentation level is the same as the opening '"json": {'
                                if indentation == json_indentation:
                                    # Join the json_lines and print the result
                                    json_string = ''.join(json_lines)
                                    jsonsFile.write(json_string)

                                    # Reset variables for the next JSON block
                                    json_started = False
                                    json_lines = []
