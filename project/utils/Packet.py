class Packet:
    preambula = "1010101"
    dest = None
    src = None
    type_of_data = None  # MESSAGE lub ARQ
    data = None  # BITY lub (ACK/NACK)
    crc32 = None

    def __init__(self, dest, src, type_of_data, data):
        self.dest = dest
        self.src = src
        self.type_of_data = type_of_data
        self.data = data

    def __str__(self):
        packet = ""
        packet += self.preambula
        packet += self.dest
        packet += self.src
        packet += self.type_of_data
        packet += self.data
        if self.crc32:
            packet += self.crc32
        return packet
