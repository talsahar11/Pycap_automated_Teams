import subprocess
import concurrent.futures
from datetime import datetime

from pysharkCapture import PysharkCapture

interface = "wlx2cd05a2aaa7c"  # Replace with your desired network interface
text_output_file = "jsons.text"

# -----Runs the automated teams login in java----- #
def run_java_process():
    java_executable = 'java'
    jar_file_path = 'automate_login.jar'
    java_command = [java_executable, '-jar', jar_file_path]
    try:
        subprocess.run(java_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Java code: {e}")


# -----Runs the packet capturing process----- #
def run_json_parser_process():
    py_cap = PysharkCapture(interface, text_output_file)
    py_cap.capture_and_handle()


def create_tshark_command():
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    pcap_output_file = f"pcaps/{current_datetime}.pcap"
    command = ['tshark', '-i', interface, '-w', pcap_output_file, "-f tcp or udp"]
    subprocess.run(command, check=True)


# -----Starts each program on another process----- #
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(run_json_parser_process)
    executor.submit(create_tshark_command)
    executor.submit(run_java_process)
