import os
import random

from fastapi import UploadFile

allowed_MIME = ["image/jpeg", "image/png"]
max_image_size_KB = 2048


class ImageException(Exception):
    pass


def save_file(data: bytes, extension: str):
    name = get_random_string(10) + "." + extension
    file = open(name, "wb")
    file.write(data)
    file.close()
    return name


def get_random_string(length):
    sample_letters = 'abcdefghijklmnopqrstuvwxyz1234567890'
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))
    return result_str


async def check_image(image: UploadFile):
    if image.content_type not in allowed_MIME:
        raise ImageException()
    data = await image.read()
    if len(data) > max_image_size_KB * 1024:
        raise ImageException()


async def upload_image(image: UploadFile):
    await check_image(image)
    data = await image.read()
    extension = image.filename.split('.')[-1]
    image_url = save_file(data, extension)
    return image_url


async def reupload_image(oldFileSrc: str, image: UploadFile):
    if oldFileSrc != "":
        os.remove(oldFileSrc)
    return await upload_image(image)


def remove_image(src: str):
    if src != "":
        os.remove(src)
