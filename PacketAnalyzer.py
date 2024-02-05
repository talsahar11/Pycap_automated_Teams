import re
import json

def parse_packet(data):
    packets = []

    # Regular expression patterns
    packet_pattern = re.compile(r'Packet #(\d+)\nTimestamp: ([\d.]+)\nLength: (\d+) bytes\nJSON:\n([\s\S]*?)(?=\nPacket #|\Z)')

    for match in packet_pattern.finditer(data):
        packet_number, timestamp, length, json_data = match.groups()

        packet_info = {
            "packetNumber": int(packet_number),
            "timestamp": float(timestamp),
            "length": int(length),
            "jsonData": parse_json(json_data.strip())
        }

        packets.append(packet_info)

    return packets

def parse_json(json_data):
    stack = []
    current_dict = {}
    array_flag = False

    for line in json_data.split('\n'):
        indent_level = line.count('\t')

        key_value = re.match(r'\s*([^:]+):\s*(.+)', line)
        if key_value:
            key, value = key_value.groups()

            if value == 'Object':
                new_dict = {}
                if array_flag:
                    current_dict.append(new_dict)
                else:
                    current_dict[key] = new_dict
                stack.append((current_dict, key))
                current_dict = new_dict
                array_flag = False
            elif value == 'Array':
                new_array = []
                if array_flag:
                    current_dict.append(new_array)
                else:
                    current_dict[key] = new_array
                stack.append((current_dict, key))
                current_dict = new_array
                array_flag = True
            elif value == 'True':
                current_dict[key] = True
            elif value == 'False':
                current_dict[key] = False
            elif value == 'Null':
                current_dict[key] = None
            elif value.startswith('String value'):
                current_dict[key] = value.split(':')[-1].strip()
            elif value.startswith('Number value'):
                current_dict[key] = float(value.split(':')[-1].strip())

        while indent_level < len(stack):
            current_dict, key = stack.pop()

        if array_flag:
            array_flag = False

    return current_dict

def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

# Example usage with the provided data file
file_path = "captured_packets.txt"
data = read_data_from_file(file_path)
formatted_packets = parse_packet(data)

# Convert the formatted packets to a JSON-formatted string
json_output = json.dumps(formatted_packets, indent=2)
print(json_output)





