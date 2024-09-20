import logging
import os
import argparse
import threading

from file_builder import FileBuilder, FileUtils
from file_model import FileModel
from json_parser import JsonParser
from database_manager import DatabaseManager


logging.basicConfig(filename='photo_anaylyzer.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

def processFile(path: str, export_path: str, file: str) -> FileModel:
    fileModel = FileModel(path, export_path, file, FileUtils.removeExtension(file) + '.json')
    if FileUtils.shouldProcess(fileModel):
        JsonParser.exportJson(fileModel.source_file, fileModel.json_file)
        FileBuilder.parseExifJson(JsonParser.parseFile(fileModel), fileModel)
        FileUtils.copyFile(fileModel)
        FileUtils.removeFile(fileModel.json_file)
    DatabaseManager.write_date(fileModel.toString())
    return fileModel

def process(root_path: str, export_path: str):
    if FileUtils.directories_not_null([root_path, export_path]):
        for path, dirs, files in os.walk(root_path):
            for file in files:
                    threading.Thread(target=processFile, args=[path, export_path, file]).start()
    else:
        raise Exception("Please make sure you pass two directories. Add --help as an argument for more information.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=FileUtils.is_valid_directory, 
                        help='The directory where you want to read the photos from.')
    parser.add_argument('--output', type=FileUtils.is_valid_directory,
                        help='The directory where you want to write the photos from.')
    args = vars(parser.parse_args())
    DatabaseManager.create_tables()
    process(JsonParser.parseData(args, 'src'), JsonParser.parseData(args, 'output'))

if __name__ == "__main__":
    main()