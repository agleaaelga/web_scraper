"""The script add custom comments to .jpg files"""

from PIL import Image
from PIL import ImageDraw, ImageFont

import piexif
import piexif.helper

import os


def break_text(txt, font, max_width):
    # We share the subset to remember the last finest guess over
    # the text breakpoint and make it faster
    subset = len(txt)
    letter_size = None

    text_size = len(txt)
    while text_size > 0:

        # Let's find the appropriate subset size
        while True:
            width, height = font.getsize(txt[:subset])
            letter_size = width / subset

            # min/max(..., subset +/- 1) are to avoid looping infinitely over a wrong value
            if width < max_width - letter_size and text_size >= subset:  # Too short
                subset = max(int(max_width * subset / width), subset + 1)
            elif width > max_width:  # Too large
                subset = min(int(max_width * subset / width), subset - 1)
            else:  # Subset fits, we exit
                break

        yield txt[:subset]
        txt = txt[subset:]
        text_size = len(txt)


def comment_jpg(filename, comment_str, path=os.path.curdir):
    img = Image.open(filename)
    if img.format != 'JPEG':
        raise Exception('Error: Given file is neither JPEG.')

    os.chdir(path)
    user_comment = piexif.helper.UserComment.dump(f'{comment_str}')
    exif_dict = piexif.load(filename)
    exif_dict['Exif'][piexif.ExifIFD.UserComment] = user_comment
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filename)
