import pyshark


class PysharkCapture:
    # ------Preference (web interface, jsons output file and uds streams dict)---------#
    udp_streams = dict()

    def __init__(self, web_interface, text_output_file):
        self.webInterface = web_interface
        self.textOutputFile = text_output_file

    # ------When udp packet arrives, the key of the ip address of the other side in the packet, will be increased by 1-#
    # ------This will allow us to determine which stream is the one we are looking for                             ----#
    def handle_udp(self, packet):
        self.udp_streams.values()

    # ------Propagates the packet towards the right handler, whether its http/json packet or udp packet-----#
    def classify_and_handle_packet(self, packet):
        for layer in packet.layers:
            if layer.layer_name == 'udp':
                self.handle_udp(packet)
            if layer.layer_name == 'json' or layer.layer_name == 'http' or layer.layer_name == 'http2':
                self.handle_json_and_http(packet)

    # ------Parsing and reformatting the data acquired from jsons and http requests------
    def handle_json_and_http(self, packet):
        with open(self.textOutputFile, 'a') as file:
            # file.write(f"Packet #{packet.number}\n")
            # file.write(f"Timestamp: {packet.sniff_timestamp}\n")
            # file.write(f"Length: {packet.length} bytes\n")
            # file.write(f"Packet--------------------------------------------------{packet}\n\n")
            # # Find the target layer
            for layer in packet.layers:
                print(layer.layer_name)
                if layer.layer_name == "json":
                    file.write(f"JSON: \n{layer}\n")
                # if layer.layer_name == "http2":
                    # file.write(f"HTTP: \n {layer}\n")
            #         break

    # -----Initiates the whole process----- #
    def capture_and_handle(self):
        try:
            capture = pyshark.LiveCapture(interface=self.webInterface, display_filter="json", use_json=True)
            for packet in capture.sniff_continuously():  # Adjust packet_count as needed
                self.classify_and_handle_packet(packet)
        except KeyboardInterrupt:
            print("Capture stopped by the user.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            import traceback
            traceback.print_exc()

