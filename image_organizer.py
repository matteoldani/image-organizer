import os
from PIL import Image
from PIL.ExifTags import TAGS
import piexif

DATETIME_ID = 36868

def is_image(file: str):
    if file.endswith(".PNG"):
        return True
    if file.endswith(".png"):
        return True
    if file.endswith(".JPG"):
        return True
    if file.endswith(".jpg"):
        return True
    if file.endswith(".jpeg"):
        return True
    if file.endswith(".JPEG"):
        return True
    if file.endswith(".HEIC"):
        return True
    if file.endswith(".heic"):
        return True
    if file.endswith(".PNG"):
        return True
    return False

def parse_datetime(datetime: str) -> dict:
    result = {}
    values = datetime.split(" ")

    date = values[0].split(":")
    result['year'] = date[0]
    result['month'] = date[1]
    result['day'] = date[2]

    time = values[1].split(":")
    result['hour'] = time[0]
    result['minute'] = time[1]
    result['second'] = time[2]

    return result

def extract_image_data(path: str) -> dict:
    return None

def organize_image(path: str, dest: str):
    image = Image.open(path)
    exifdata = image.getexif()
    exif_dict = piexif.load(path)
    print(exif_dict)
    
    value = exif_dict['Exif'][DATETIME_ID].decode()
    
    print(parse_datetime(value))

def organize(path: str, destination: str, recursive: bool):
    if recursive:
        for (dirpath, dirnames, filenames) in os.walk(path):
            for f in filenames:
                if is_image(f):
                    print(f)
                    organize_image(os.path.join(dirpath, f), destination)
    else:
        filenames = os.listdir(path)
        for f in filenames:
            if os.path.isfile(f) and is_image(f):
                organize_image(os.path.join(path, f), destination)
