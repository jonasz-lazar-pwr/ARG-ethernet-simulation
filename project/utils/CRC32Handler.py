import binascii


def generate_ethernet_crc32(data):
    padded_data = data
    # dopasuj długość danych do wielokrotności 32 bitów
    data_length = len(padded_data)
    if data_length % 32 != 0:
        padding_length = 32 - data_length % 32
        padded_data += '0' * padding_length
    # konwertuj dane do postaci bajtowej
    byte_data = binascii.unhexlify(hex(int(padded_data, 2))[2:].zfill(len(padded_data) // 4))
    # oblicz CRC32
    crc32 = binascii.crc32(byte_data) & 0xffffffff
    # konwertuj CRC32 na postać binarną
    crc32_bin = bin(crc32)[2:].zfill(32)
    # zwróć CRC32 w postaci binarnej
    return crc32_bin


def compare_crc32(packet):
    generated_crc32 = generate_ethernet_crc32(packet.data)
    return packet.crc32 == generated_crc32
