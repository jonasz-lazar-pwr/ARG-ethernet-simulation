import random


class TransmissionLine:
    error_coefficient = 5
    PCs = []
    line_MESSAGE = 0
    line_ACK = 0
    line_NACK = 0
    time_to_free = 0.0

    def send(self, packet):
        modified_packet = packet
        if packet.type_of_data == "MESSAGE":
            modified_packet = self.generate_noise(self=self, packet=packet)

        for pc in self.PCs:
            if pc.mac_address == modified_packet.dest:
                return pc.receive_packet(modified_packet)

    def generate_noise(self, packet):
        noised_message = ""
        for b in packet.data:
            if random.randint(0, 100) <= self.error_coefficient:
                if b == '1':
                    noised_message += '0'
                elif b == '0':
                    noised_message += '1'
            else:
                noised_message += b
        packet.data = noised_message

        return packet
