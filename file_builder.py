import json
from database_manager import DatabaseManager
from json_parser import JsonParser

from file_model import FileModel


class FileBuilder:

    def parseExifJson(json_object: json, fileModel: FileModel):
        fileModel.create_date = JsonParser.parseDate(json_object, fileModel.file_name)
        fileModel.destination_path = FileUtils.createDirectories(fileModel.export_path, fileModel.create_date)
        fileModel.file_size = JsonParser.parseData(json_object, 'FileSize')
        fileModel.x_resolution = JsonParser.parseData(json_object, 'XResolution')
        fileModel.y_resolution = JsonParser.parseData(json_object, 'YResolution')
        fileModel.is_exact_copy = FileBuilder.calculateDuplicate(fileModel)

    def calculateDuplicate(fileModel: FileModel):
        if FileUtils.fileFileExists(fileModel):
            fileModel.file_exits = True
            results: json = DatabaseManager.fetch_row(fileModel.file_name)
            valid_array = (isinstance(results, list) and len(results) > 0)
            if valid_array: 
                return (FileBuilder.compare(fileModel.x_resolution, JsonParser.parseData(results, 'x_resolution'))
                        and FileBuilder.compare(fileModel.y_resolution, JsonParser.parseData(results, 'y_resolution'))
                        and FileBuilder.compare(fileModel.file_size, JsonParser.parseData(results, 'file_size')))

    def compare(value1, value2):
        return str(value1) == str(value2)




import os
import filetype
from pathlib import Path
import shutil
from datetime import datetime
import random

class FileUtils:

    def unZip(path: str, file: str):
        shutil.unpack_archive(path + os.sep + file, path + os.sep + FileUtils.removeExtension(file))

    def shouldProcess(fileModel: FileModel):
        if filetype.is_image(fileModel.source_file):
            fileModel.export_path = fileModel.export_path + os.sep + 'pic'
        if filetype.is_video(fileModel.source_file):
            fileModel.export_path = fileModel.export_path + os.sep + 'video'
        return filetype.is_image(fileModel.source_file) or filetype.is_video(fileModel.source_file)

    def createDirectories(export_path: str, date: datetime): 
        directory = export_path + os.sep + date.strftime("%Y") + os.sep + date.strftime("%Y") + '_' + date.strftime("%m")
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def copyFile(fileModel: FileModel):
        if fileModel.file_exits == False:
            shutil.copy2(fileModel.source_path + os.sep + fileModel.file_name, fileModel.destination_path + os.sep + fileModel.file_name)
            fileModel.is_written = True
        elif fileModel.file_exits == True and fileModel.is_exact_copy == False:
            new_file_name = Path(fileModel.file_name).stem + "_".join([str(random.randint(0, 999)).zfill(3) for _ in range(2)]) + Path(fileModel.file_name).suffix
            shutil.copy2(fileModel.source_path + os.sep + fileModel.file_name, fileModel.destination_path + os.sep + new_file_name)
            fileModel.is_written = True

    def removeExtension(file: str):
        return os.sep + Path(file).stem

    def removeFile(json_path: str):
        os.remove(json_path)

    def fileFileExists(fileModel: FileModel):
        return Path(fileModel.destination_path + '\\' + fileModel.file_name).is_file()

    def is_valid_directory(path):
        if os.path.isdir(path):
            return path
        else:
            raise NotADirectoryError(path)
        
    def directories_not_null(directories: list):
        for directory in directories:
            if os.path.isdir(directory) == False:
                return False
        return True
        


