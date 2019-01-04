#!/usr/bin/env python

from random import randint
from PIL import Image
from bitarray import bitarray

width = 86
height = 86

# Create empty data.

gen_data = width * height * bitarray('0')

def put_gen_data(x, y, val):
    gen_data[y * width + x] = val

def get_gen_data(x, y):
    if gen_data[y * width + x]:
        return 1
    else:
        return 0

# Plant initial state.

#put_gen_data(width/2, 0, 1)

for i in range(0, width):
    if i % 3 == 0:
        put_gen_data(i, 0, randint(0, 1))

# Generate data.

def apply_rule(pattern):

    p = pattern

    # Rule 90.
    # http://edinburghhacklab.com/2013/12/weaving-wolfram-rule-90/

    if p[0] == 0 and p[1] == 0 and p[2] == 0:
        return 0

    if p[0] == 0 and p[1] == 0 and p[2] == 1:
        return 1

    if p[0] == 0 and p[1] == 1 and p[2] == 0:
        return 0

    if p[0] == 0 and p[1] == 1 and p[2] == 1:
        return 1

    if p[0] == 1 and p[1] == 0 and p[2] == 0:
        return 1

    if p[0] == 1 and p[1] == 0 and p[2] == 1:
        return 0

    if p[0] == 1 and p[1] == 1 and p[2] == 0:
        return 1

    if p[0] == 1 and p[1] == 1 and p[2] == 1:
        return 0

    print("Error!")
    return 5

def get_wrapped_x_coord(x):
    while x >= width:
        x -= width
    while x < 0:
        x += width
    return x

finished = False

for y in range(height):

    # Skip initial row.

    if y == 0:
        continue

    for x in range(width):

        pattern = (
            get_gen_data(get_wrapped_x_coord(x - 1), y - 1),
            get_gen_data(x, y - 1),
            get_gen_data(get_wrapped_x_coord(x + 1), y - 1)
        )

        put_gen_data(x, y, apply_rule(pattern))

print("Generated data")

# Generate image from data.

def pixel_from_datum(i):
    return ((1-i) * 255, (1-i) * 255, (1-i) * 255)

img_data = []

for y in range(0, height):
    for x in range(0, width):
            p = pixel_from_datum(get_gen_data(x, y))
            img_data.append(p)

img = Image.new('RGB', (width, height))
img.putdata(img_data)
image_name = 'image.png'
img.save(image_name)

print("Generated image '" + image_name + "'")