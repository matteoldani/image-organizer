import os
import shutil
from exif import Image
import pprint
import logging

image_stats = {}
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG)

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

def move_image(path: str, datetime: dict, destination: str):
    new_name = f"IMG-{datetime['year']}{datetime['month']}{datetime['day']}"
    _, extension = os.path.splitext(path)
    seq_number = f"{image_stats[datetime['year']][datetime['month']]:04}"
    final_file_path = f"{destination}/{datetime['year']}/{datetime['month']}/{new_name}-{seq_number}{extension}"

    logging.debug("new file path: %s", final_file_path)
    # check if the forlder for the corresponding year/month exists
    if not os.path.isdir(f"{destination}/{datetime['year']}/{datetime['month']}"):
         os.makedirs(f"{destination}/{datetime['year']}/{datetime['month']}")

    # move the image inside
    shutil.move(path, final_file_path)

def move_unordered(path: str, destination: str):
    if not os.path.isdir(f"{destination}/unordered"):
        os.makedirs(f"{destination}/unordered")

    file_name = path.split('/')
    file_name = file_name[-1]
    unordered_path = destination + file_name
    logging.debug("Unordered path of %s is %s", path, unordered_path)
    shutil.move(path, unordered_path)

def extract_image_data(path: str) -> dict:
    try:
        with open(path, 'rb') as img_file: 
            img = Image(img_file)
            # x = (img.get('datetime'))
            if img.has_exif:
                raw_datetime = (img.get('datetime_original'))
                datetime = parse_datetime(raw_datetime)
                return datetime
            else:
                logging.error(f'{path} does not have EXIF, moved to unordered')
                return None
    except:
        logging.error(f"{path} gave an exception, move to unordered")
        return None

def organize_image(path: str, dest: str):
    
    datetime = extract_image_data(path)
    if datetime == None: 
        move_unordered(path, dest)
        return

    # update stats
    if datetime['year'] not in image_stats:
        image_stats[datetime['year']] = {}
    if datetime['month'] not in image_stats[datetime['year']]:
        image_stats[datetime['year']][datetime["month"]] = 0

    image_stats[datetime['year']][datetime['month']] += 1

    # move the image to the final location
    move_image(path, datetime, dest)

def organize(path: str, destination: str, recursive: bool):
    if recursive:
        for (dirpath, dirnames, filenames) in os.walk(path):
            for f in filenames:
                if is_image(f):
                    organize_image(os.path.join(dirpath, f), destination)
    else:
        filenames = os.listdir(path)
        for f in filenames:
            if os.path.isfile(f) and is_image(f):
                organize_image(os.path.join(path, f), destination)

    # print the image stats 
    pprint.pprint(image_stats)
