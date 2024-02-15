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
            print(packet.layers)
            layer = packet.layers.http2
            print(layer)
            if len(packet.get_multiple_layers('http2')) != 1:
                print("Http layers: ", len(packet.get_multiple_layers('http2')))

        for layer in packet.layers:
            print(f"LayerName: {layer.layer_name} ------- Fields: {layer.field_names} --------")

            if layer.layer_name == "json":
                # file.write(f"JSON Number { self.j }: \n{layer}\n")
                break
            if layer.layer_name == "http2":
                print()
                # # Check if the frame contains payload data
                # if 'Raw' in frame:
                #     raw_data = frame['Raw'].load
                #     file.write(f"Raw Data: {raw_data}\n")
                #     # You can further process or attempt to parse the JSON here



    # -----Initiates the whole process----- #
    def capture_and_handle(self):
        try:
            i = 0
            capture = pyshark.LiveCapture(interface=self.webInterface, display_filter='json')
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

