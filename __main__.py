import argparse
import os
from image_organizer import organize
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.DEBUG)

def validate_path(path: str) -> bool:
    try:
        abs_path = os.path.abspath(path)
        return True
    except:
        return False
        

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", 
                            help="Specify the path of the directory containing the photos to be organized",
                            required=True)
    parser.add_argument("-d", "--destination",
                            help="Path of the organized photos",
                            required=True)
    parser.add_argument("-r", "--recursive",
                            action="store_true", 
                            help="If present also images in subfolders will be organized")
    args = parser.parse_args()
    if validate_path(args.path) and validate_path(args.destination):
        abs_path = os.path.abspath(args.path)
        abs_dest = os.path.abspath(args.destination)
        organize(abs_path, abs_dest, recursive=args.recursive)
    else:
        logging.error("The path provided is not valid, exiting...")
    
if __name__ == '__main__':
    main()