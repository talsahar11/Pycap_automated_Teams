import pyshark


class PysharkCapture:
    # ------Preference (web interface, jsons output file and uds streams dict)---------#
    udp_streams = dict()

    def __init__(self, web_interface, text_output_file):
        self.webInterface = web_interface
        self.textOutputFile = text_output_file

    # ------Parsing and reformatting the data acquired from jsons and http requests------
    j = 0
    def handle_json_and_http(self, packet):
        with open(self.textOutputFile, 'a') as file:
            self.j += 1
            # file.write(f"Packet #{packet.number}\n")
            # file.write(f"Timestamp: {packet.sniff_timestamp}\n")
            # file.write(f"Length: {packet.length} bytes\n")
            # file.write(f"Packet--------------------------------------------------{packet}\n\n")
            # # Find the target layer
            for layer in packet.layers:
                if layer.layer_name == "json":
                    file.write(f"JSON Number { self.j }: \n{layer}\n")
                    break
                if layer.layer_name == "http2":
                    file.write(f"httpo { self.j }: \n{layer}\n")
                    print(packet.layers[-1])


    # -----Initiates the whole process----- #
    def capture_and_handle(self):
        try:
            i = 0
            capture = pyshark.LiveCapture(interface=self.webInterface, display_filter='json', use_json=True)
            for packet in capture.sniff_continuously():  # Adjust packet_count as needed
                self.handle_json_and_http(packet)
                print("Shiittty i: ", i)
                i += 1
        except KeyboardInterrupt:
            print("Capture stopped by the user.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            import traceback
            traceback.print_exc()

