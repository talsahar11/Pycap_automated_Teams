import json
import subprocess
import threading

interface = "wlx2cd05a2aaa7c"  # Replace with your network interface
pcap_output_file_template = "pcaps/shit.pcap"  # Template for naming pcap files
capture_interval = 10  # Interval in seconds for capturing

def live_capture():
    output_file = "output.txt"  # File to redirect stdout to
    command = ['tshark', '-i', interface, '-w', pcap_output_file_template, '-f', 'tcp or udp', "-V", "-T", "json"]
    with open(output_file, "w") as f:
        subprocess.run(command, check=True, stdout=f)

def main():
    # Start scheduled capture process
    capture_thread = threading.Thread(target=live_capture)
    capture_thread.start()
    command = ['java', '-jar', "automate_login.jar"]
    subprocess.run(command, check=True)

def analyze_text_file(file_path):
    json_started = False
    json_lines = []
    json_indentation = 0
    with open("stripped_jsons", 'w') as jsonFile:
        with open(file_path, 'r') as file:
            for line in file:
                # Count leading whitespace characters to determine indentation level
                indentation = len(line) - len(line.lstrip())

                # Strip whitespace from the beginning and end of the line
                stripped_line = line.strip()

                # Check if the line contains '"json": {'
                if stripped_line == '"json": {':
                    json_started = True
                    json_lines.append(line)
                    json_indentation = indentation
                    continue  # Skip to the next line

                # If JSON parsing has started, append the line to json_lines
                if json_started:
                    json_lines.append(line)

                    # Check if the line contains a closing '}'
                    if stripped_line == '}' or stripped_line == '},':
                        # Check if the indentation level is the same as the opening '"json": {'
                        if indentation == json_indentation:
                            # Join the json_lines and print the result
                            json_string = ''.join(json_lines)
                            jsonFile.write(json_string)
    
                            # Reset variables for the next JSON block
                            json_started = False
                            json_lines = []

if __name__ == "__main__":
    analyze_text_file("output.txt")

