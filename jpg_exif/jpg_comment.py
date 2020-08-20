"""The script add custom comments to .jpg files"""

from PIL import Image
import piexif
import piexif.helper
import os


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



def caption_jpg():
    pass

