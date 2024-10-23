from PIL import Image
import math
import os
import struct

pcap_directory = './pcap/'
image_width = 28

# this function converts a pcap file into an image
def pcap_to_image(filename):
    pixels = []

    # read the pcap file as packets
    with open(pcap_directory + filename, 'rb') as f:
        global_header = f.read(24)

        magic_number, version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack('IHHiIII', global_header)

        packet_num = 1
        while True:
            packet_header = f.read(16)
            if len(packet_header) < 16:
                break

            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', packet_header)
            packet_data = f.read(incl_len)

            for byte in packet_data:
                if len(pixels) < image_width * image_width :
                    pixels.append((int(byte), int(byte), int(byte)))
            packet_num += 1

    image = Image.new("RGB", (image_width, image_width))
    image.putdata(pixels)
    image.save('./png/' + filename + '.png')

# foreach file in pcap directory, convert the file to an image and output it in /png directory
for filename in os.listdir(pcap_directory):

    file_path = os.path.join(pcap_directory, filename)

    if os.path.isfile(file_path):
        pcap_to_image(filename)