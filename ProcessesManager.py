import subprocess
import concurrent.futures

from pysharkCapture import PysharkCapture


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
def run_pyshark_process():
    py_cap = PysharkCapture()
    py_cap.capture_and_handle()


# -----Starts each program on another process----- #
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(run_pyshark_process)
    executor.submit(run_java_process())
