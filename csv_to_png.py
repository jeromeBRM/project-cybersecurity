import pandas as pd
from PIL import Image
import math
import os

csv_directory = './csv/'
image_width = 16

time_ranges = [0, 3, 7, 12, 18, 25, 33, 42, 100, 200]

api_categories = [
    'network',
    'registry',
    'service',
    'file',
    'hardware and system',
    'message',
    'process',
    'system',
    'Shellcode',
    'Keylogging',
    'Obfuscation',
    'synchronisation',
    'resource',
    'exception',
    'ole',
    'misc'
]

hex_color_map = [
    ['#FFFFFF', '#FFC1E0', '#FFAAD5', '#FF95CA', '#FF79BC', '#FF60AF', '#FF359A', '#FF0080', '#F00078', '#D9006C', '#BF0060'],
    ['#FFFFFF', '#FFBFFF', '#FFA6FF', '#FF8EFF', '#FF77FF', '#FF44FF', '#FF00FF', '#E800E8', '#D200D2', '#AE00AE', '#930093'],
    ['#FFFFFF', '#FFDAC8', '#FFCBB3', '#FFBD9D', '#FFAD86', '#FF9D6F', '#FF8F59', '#FF8040', '#FF5809', '#F75000', '#D94600'],
    ['#FFFFFF', '#D3FF93', '#CCFF80', '#B7FF4A', '#A8FF24', '#9AFF02', '#8CEA00', '#82D900', '#73BF00', '#64A600', '#548C00'],
    ['#FFFFFF', '#CAFFFF', '#BBFFFF', '#A6FFFF', '#4DFFFF', '#00FFFF', '#00E3E3', '#00CACA', '#00AEAE', '#009393', '#005757'],
    ['#FFFFFF', '#C1FFE4', '#ADFEDC', '#96FED1', '#4EFEB3', '#1AFD9C', '#02F78E', '#02DF82', '#01B468', '#019858', '#01814A'],
    ['#FFFFFF', '#D6D6AD', '#CDCD9A', '#C2C287', '#B9B973', '#AFAF61', '#A5A552', '#949449', '#808040', '#707038', '#616130'],
    ['#FFFFFF', '#DCB5FF', '#D3A4FF', '#CA8EFF', '#BE77FF', '#B15BFF', '#9F35FF', '#921AFF', '#8600FF', '#6E00FF', '#5B00AE'],
    ['#FFFFFF', '#FFFF6F', '#FFFF37', '#F9F900', '#E1E100', '#C4C400', '#A6A600', '#8C8C00', '#737300', '#5B5B00', '#5B5B00'],
    ['#FFFFFF', '#FFE66F', '#FFE153', '#FFDC35', '#FFD306', '#EAC100', '#D9B300', '#C6A300', '#AE8F00', '#977C00', '#796400'],
    ['#FFFFFF', '#D8D8EB', '#C7C7E2', '#B8B8DC', '#A6A6D2', '#9999CC', '#8080C0', '#7373B9', '#5A5AAD', '#5151A2', '#484891'],
    ['#FFFFFF', '#97CBFF', '#84C1FF', '#66B3FF', '#46A3FF', '#2894FF', '#0080FF', '#0072E3', '#0066CC', '#005AB5', '#004B97'],
    ['#FFFFFF', '#B9B9FF', '#AAAAFF', '#9393FF', '#7D7DFF', '#6A6AFF', '#4A4AFF', '#2828FF', '#0000E3', '#0000C6', '#0000C6'],
    ['#FFFFFF', '#FFD1A4', '#FFC78E', '#FFBB77', '#FFAF60', '#FFA042', '#FF9224', '#FF8000', '#EA7500', '#D26900', '#BB5E00'],
    ['#FFFFFF', '#FF9797', '#FF7575', '#FF5151', '#FF2D2D', '#FF0000', '#EA0000', '#CE0000', '#AE0000', '#930000', '#750000'],
    ['#FFFFFF', '#93FF93', '#79FF79', '#53FF53', '#28FF28', '#00EC00', '#00DB00', '#00BB00', '#00A600', '#009100', '#007500']
]

def find_floor_index(number):
    floor_index = 0
    for i in range(len(time_ranges)):
        if time_ranges[i] < number:
            floor_index+=1
    return floor_index

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb

# this function converts a csv file into an image
def csv_to_image(filename):
    df = pd.read_csv(csv_directory + filename)

    start_time = df.iloc[0, -1]
    end_time = df.iloc[-1, -1]
    run_time = end_time - start_time
    unit_time = run_time / 16

    #distinct_categories = df['category'].unique()
    #print(distinct_categories)

    pixels = []

    for i in range(image_width):
        for u in range(image_width):
            filtered = df[(df['time'] - start_time >= u * unit_time) & (df['time'] - start_time < (u + 1) * unit_time) & (df['category'] == api_categories[i])]
            pixels.append(hex_to_rgb(hex_color_map[i][find_floor_index(len(filtered))]))

    image = Image.new("RGB", (image_width, image_width))
    image.putdata(pixels)
    image.save('./png/' + filename + '.png')

# foreach file in csv directory, convert the file to an image and output it in /png directory
for filename in os.listdir(csv_directory):

    file_path = os.path.join(csv_directory, filename)

    if os.path.isfile(file_path):
        csv_to_image(filename)