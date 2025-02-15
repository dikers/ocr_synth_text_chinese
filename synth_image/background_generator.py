import cv2
import math
import os
import random as rnd
import numpy as np
import time

from PIL import Image, ImageDraw, ImageFilter


def gaussian_noise(height, width):
    """
        Create a background with Gaussian noise (to mimic paper)
    """

    # We create an all white image
    image = np.ones((height, width)) * 255

    # We add gaussian noise
    cv2.randn(image, 235, 8 + rnd.randint(1, 10))

    _draw_line(image, height, width)

    return Image.fromarray(image).convert("RGBA")


def plain_white(height, width):
    """
        Create a plain white background
    """
    image = np.ones((height, width)) * 255
    _draw_line(image, height, width)

    return Image.fromarray(image).convert("RGBA")


def quasicrystal(height, width):
    """
        Create a background with quasicrystal (https://en.wikipedia.org/wiki/Quasicrystal)
    """

    image = Image.new("L", (width, height))
    pixels = image.load()

    frequency = rnd.random() * 30 + 20  # frequency
    phase = rnd.random() * 2 * math.pi  # phase
    rotation_count = rnd.randint(10, 20)  # of rotations

    for kw in range(width):
        y = float(kw) / (width - 1) * 4 * math.pi - 2 * math.pi
        for kh in range(height):
            x = float(kh) / (height - 1) * 4 * math.pi - 2 * math.pi
            z = 0.0
            for i in range(rotation_count):
                r = math.hypot(x, y)
                a = math.atan2(y, x) + i * math.pi * 2.0 / rotation_count
                z += math.cos(r * math.sin(a) * frequency + phase)
            c = int(255 - round(255 * z / rotation_count))
            pixels[kw, kh] = c  # grayscale
    return image.convert("RGBA")


def image(height, width, image_dir):
    """
        Create a background with a image
    """
    images = os.listdir(image_dir)

    if len(images) > 0:
        pic = Image.open(
            os.path.join(image_dir, images[rnd.randint(0, len(images) - 1)])
        )

        if pic.size[0] < width:
            pic = pic.resize(
                [width, int(pic.size[1] * (width / pic.size[0]))], Image.ANTIALIAS
            )
        if pic.size[1] < height:
            pic = pic.resize(
                [int(pic.size[0] * (height / pic.size[1])), height], Image.ANTIALIAS
            )

        if pic.size[0] == width:
            x = 0
        else:
            x = rnd.randint(0, pic.size[0] - width)
        if pic.size[1] == height:
            y = 0
        else:
            y = rnd.randint(0, pic.size[1] - height)

        return pic.crop((x, y, x + width, y + height))
    else:
        raise Exception("No images where found in the images folder!")


def _draw_line(draw_image, height, width):
    rnd.seed(time.time())
    rand_seed = rnd.randint(0, 3)
    if rand_seed % 2 == 1:
        return

    top = rnd.randint(10, 20)
    for index in range(20):
        left = rnd.randint(10, 80)
        right = width - rnd.randint(10, 80)
        top = top + rnd.randint(40, 150)
        if top > height:
            break
        cv2.line(draw_image, (left, top), (right, top), (0, 255, 0), 1)


    left = rnd.randint(10, 80)

    for index in range(20):
        left = left + rnd.randint(60, 250)
        top = rnd.randint(10, 80)
        bottom = height - rnd.randint(10, 80)
        if left > width:
            break
        cv2.line(draw_image, (left, top), (left, bottom), (0, 255, 0), 1)
