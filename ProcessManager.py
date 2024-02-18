import os
import signal
import subprocess
import multiprocessing
import threading
import sys
import traceback

from JsonKeysGrabber import JsonKeysGrabber
from JsonStripper import JsonStripper

tshark_output_file = "tshark_output.txt"
json_stripper_output_file = "json_stripper_output.txt"
files = [tshark_output_file, json_stripper_output_file]


class ProcessManager:
    def __init__(self):

        self.interface = "wlx2cd05a2aaa7c"
        self.pcap_output_file = "pcaps/record.pcap"
        self.seleniumProcess = multiprocessing.Process(target=self.__runSelenium)
        self.tsharkProcess = multiprocessing.Process(target=self.__runTshark)
        self.jsonStripperProcess = multiprocessing.Process(target=self.__runJsonStripper)
        self.jsonKeysGrabberProcess = multiprocessing.Process(target=self.__runJsonKeysGrabber)
        self.processes = [self.seleniumProcess, self.tsharkProcess, self.jsonStripperProcess,
                          self.jsonKeysGrabberProcess]
        self.stop_event = threading.Event()  # Event to signal termination

    def start(self):
        for process in self.processes:
            process.start()

    def __runSelenium(self):
        try:
            command = ['java', '-jar', "automate_login.jar"]
            subprocess.run(command, check=True)
        except Exception as e:
            print("Something wrong with selenium process")

    def __runTshark(self):
        try:
            command = ['tshark', '-i', self.interface, '-w', self.pcap_output_file, '-f', 'tcp','-V', "-T", "json"]
            with open(tshark_output_file, "w") as f:
                subprocess.run(command, check=True, stdout=f)
        except Exception as e:
            print("Something wrong with tshark process")

    def __runJsonStripper(self):
        try:
            stripper = JsonStripper(tshark_output_file, json_stripper_output_file)
            stripper.run()
        except Exception as e:
            print(f"Something wrong with the json stripper, Error: {traceback.print_exc()}")
            self.shutdown()

    def __runJsonKeysGrabber(self):
        try:
            keysGrabber = JsonKeysGrabber(json_stripper_output_file)
            keysGrabber.start()
        except Exception as e:
            print("Something wrong with Json key grabber process")

    def shutdown(self):
        for process in reversed(self.processes):
            process.terminate()


def create_files():
    for file in files:
        with open(file, 'w'):
            pass


def cleanup():
    for file in files:
        os.remove(file)



main_pid = os.getpid()
pm = ProcessManager()


create_files()
def sigint_handler(sig, frame):
    print("SIGINT received. Exiting gracefully.")
    # Get the process ID of the current process
    current_pid = os.getpid()
    # if current_pid == main_pid:
        # cleanup()
    # Terminate the current process
    os.kill(current_pid, signal.SIGTERM)
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)
pm.start()
