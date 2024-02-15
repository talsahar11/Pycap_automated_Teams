import subprocess
import multiprocessing


class ProcessManager:
    def __init__(self):
        self.interface = "wlx2cd05a2aaa7c"
        self.pcap_output_file = "pcaps/record.pcap"

    def start(self):
        seleniumProcess = multiprocessing.Process(target=self.__runSelenium)
        tsharkProcess = multiprocessing.Process(target=self.__runTshark)
        jsonStripperProcess = multiprocessing.Process(target=self.__runJsonStripper)
        tsharkProcess.start()
        seleniumProcess.start()
        jsonStripperProcess.start()

    def __runSelenium(self):
        command = ['java', '-jar', "automate_login.jar"]
        subprocess.run(command, check=True)

    def __runTshark(self):
        output_file = "output.txt"  # File to redirect stdout to
        command = ['tshark', '-i', self.interface, '-w', self.pcap_output_file, '-f', 'tcp or udp', "-V", "-T", "json"]
        with open(output_file, "w") as f:
            subprocess.run(command, check=True, stdout=f)

    def __runJsonStripper(self):
        print()


pm = ProcessManager()
pm.start()