from project.utils.CRC32Handler import generate_ethernet_crc32, compare_crc32
from project.utils.Packet import Packet
import copy


class PC:
    transmission_line = None
    mac_address = None
    last_packet = None

    def __init__(self, mac_address, transmission_line):
        self.mac_address = mac_address
        self.transmission_line = transmission_line

    def encode_data(self, data):
        # TODO: kodowanie wiadomosci
        return data

    def build_packet(self, dest, type_of_data, data):
        encoded_data = self.encode_data(data)
        packet = Packet(dest, self.mac_address, type_of_data, encoded_data)
        packet.crc32 = generate_ethernet_crc32(data)
        return packet

    def send_packet(self, dest, type_of_data, data):
        if type_of_data == "MESSAGE":
            packet = self.build_packet(dest=dest, type_of_data=type_of_data, data=data)
            if self.last_packet is None:
                self.last_packet = copy.deepcopy(packet)
            # print("ostatnio wysłana wiadomość: " + self.last_packet.data)
            return self.transmission_line.send(self=self.transmission_line, packet=packet)

        elif type_of_data == "ARQ":
            packet = Packet(dest, self.mac_address, type_of_data, data)
            return self.transmission_line.send(self=self.transmission_line, packet=packet)

    def receive_packet(self, packet):

        if packet.type_of_data == "ARQ":
            if packet.data == "ACK":
                self.last_packet = None
                self.transmission_line.line_ACK += 1
                return None
            elif packet.data == "NACK":
                self.transmission_line.line_NACK += 1
                if self.last_packet:
                    return [self.mac_address, self.last_packet.dest, self.last_packet.type_of_data, self.last_packet.data]

        elif packet.type_of_data == "MESSAGE":
            self.transmission_line.line_MESSAGE += 1
            if compare_crc32(packet):
                return [self.mac_address, packet.src, "ARQ", "ACK"]
            else:
                return [self.mac_address, packet.src, "ARQ", "NACK"]

    def set_models(self, transmission_line):
        self.transmission_line = transmission_line
