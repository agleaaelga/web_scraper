from PIL import Image
from PIL import ImageDraw, ImageFont

import os


def wrap_text(text, font, max_width):
    text_width, text_height = font.getsize(text)
    char_num = len(text)
    wrap_index = int(char_num * max_width / text_width)
    num_line = text_width // max_width + 1
    return [text[i * wrap_index:(i + 1) * wrap_index] for i in range(num_line)]


def caption_jpg(filename, comment_str, path=os.path.curdir):
    os.chdir(path)
    img = Image.open(filename)
    width, height = img.size

    font_size = int(width / 40)
    font = ImageFont.truetype('arial.ttf', font_size)

    line = wrap_text(comment_str, font, width - 40)
    num_of_lines = len(line)
    multi_line = '\n'.join(line)

    img_new = Image.new('RGB', (width, height + (num_of_lines * (font_size + 3)) + 10), color='White')
    draw = ImageDraw.Draw(img_new)
    Image.Image.paste(img_new, img, (0, 0))

    draw.multiline_text((10, height + 10), multi_line, fill='Black', font=font)

    img_new.save(filename)